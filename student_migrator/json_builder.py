import math
import logging
from .mappings import get_mapping

logger = logging.getLogger(__name__)

EXCEL_ERROR_STRINGS = {
    "#n/a", "#value!", "#ref!", "#div/0!", "#null!", "#name?", "#num!",
    "nan", "null", "none", ""
}

def sanitize_flat_dict(d: dict) -> dict:
    """Sanitizes raw values (replaces float NaN and Excel error strings like #N/A with None)."""
    clean = {}
    for k, v in d.items():
        if isinstance(v, float) and math.isnan(v):
            clean[k] = None
        elif isinstance(v, str):
            v_clean = v.strip()
            if v_clean.lower() in EXCEL_ERROR_STRINGS:
                clean[k] = None
            else:
                clean[k] = v_clean
        else:
            clean[k] = v
    return clean

class RecordBuilder:
    def __init__(self, semester: int):
        self.semester = semester
        self.mapping = get_mapping(semester)

    def process_row(self, sheet_name: str, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None, dict | None]:
        """
        Processes a single Excel/CSV row dict.
        Returns (student_id, name, email, flat_record_dict).
        If both student_id and name are missing, returns (None, None, None, None) to skip non-student template/header/footer rows cleanly.
        Any row containing a student_id or name is processed, even if all evaluation metrics are NULL.
        """
        student_id, name, email = self.mapping.extract_core_fields(row_dict, row_list)
        
        # Consider the row if it has an id OR a name (or both)
        if not student_id and not name:
            return None, None, None, None

        raw_record = self.mapping.build_record(sheet_name, row_dict, row_list, student_id, name, email)
        clean_record = sanitize_flat_dict(raw_record)

        # Ensure ID primary key is populated if student_id is present
        if student_id:
            clean_record["id"] = student_id
        if name:
            clean_record["full_name"] = name
        if email:
            clean_record["college_email_id"] = email

        return student_id, name, email, clean_record

# Alias for backwards compatibility
JSONBuilder = RecordBuilder
