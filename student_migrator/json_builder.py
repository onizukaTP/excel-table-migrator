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
        If student_id is not present, returns (None, None, None, None) to skip non-student rows cleanly.
        """
        student_id, name, email = self.mapping.extract_core_fields(row_dict, row_list)
        
        if not student_id:
            return None, None, None, None

        raw_record = self.mapping.build_record(sheet_name, row_dict, row_list, student_id, name, email)
        clean_record = sanitize_flat_dict(raw_record)

        return student_id, name, email, clean_record

# Alias for backwards compatibility
JSONBuilder = RecordBuilder
