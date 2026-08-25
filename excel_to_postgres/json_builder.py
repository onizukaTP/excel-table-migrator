import json
import math
import logging
from .mappings import get_mapping

logger = logging.getLogger(__name__)

def sanitize_json_dict(d):
    """Recursively replaces any NaN float values with None for JSONB safety."""
    if isinstance(d, dict):
        return {k: sanitize_json_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [sanitize_json_dict(v) for v in d]
    elif isinstance(d, float) and math.isnan(d):
        return None
    return d

class JSONBuilder:
    def __init__(self, semester: int):
        self.semester = semester
        self.mapping = get_mapping(semester)

    def process_row(self, sheet_name: str, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None, dict | None]:
        """
        Processes a single Excel/CSV row dict.
        Returns (student_id, name, email, data_payload_dict).
        If student_id is not present, returns (None, None, None, None) to skip non-student rows cleanly.
        """
        student_id, name, email = self.mapping.extract_core_fields(row_dict, row_list)
        
        if not student_id:
            return None, None, None, None

        raw_data = self.mapping.build_json(sheet_name, row_dict, row_list)
        clean_data = sanitize_json_dict(raw_data)

        # Verify JSON serializability
        try:
            json.dumps(clean_data)
        except Exception as e:
            raise ValueError(f"Failed to serialize row data to JSON for student_id {student_id}: {e}")

        return student_id, name, email, clean_data
