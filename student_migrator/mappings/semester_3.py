import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────
# Semester 3 — Positional Column Index Map
# ──────────────────────────────────────────────────────────────────────
# The Sem 3 Excel has 115 data columns (cols 116-119 are empty padding).
# Col indices are 0-based (matching row_list position).
#
# 3 subjects with 35 columns each:
#   - String Fundamentals, String Operations & Performance and OOP Fundamentals
#   - Core OOP Principles
#   - Advanced OOP Concepts and Data Structure
#
# Each subject block (35 cols):
#   class_practice, lab_practice, assignment,
#   tech_input t1-t4, learn_input l1-l4, comm_input c1-c4,
#   tech_score t1-t4, learn_score l1-l4, level_combined,
#   comm_score c1-c4, summary_t, summary_l, summary_c,
#   total_score, help_status, coding_level, review_comments
# ──────────────────────────────────────────────────────────────────────

SEM3_COLUMNS = [
    # Common (6 cols: indices 0-5)
    "sn", "id", "full_name", "college_email_id", "assignment_submission", "engagement_status",

    # String Fundamentals (35 cols: indices 6-40)
    "string_class_practice", "string_lab_practice", "string_assignment",
    "string_tech_input_t1", "string_tech_input_t2", "string_tech_input_t3", "string_tech_input_t4",
    "string_learn_input_l1", "string_learn_input_l2", "string_learn_input_l3", "string_learn_input_l4",
    "string_comm_input_c1", "string_comm_input_c2", "string_comm_input_c3", "string_comm_input_c4",
    "string_tech_score_t1", "string_tech_score_t2", "string_tech_score_t3", "string_tech_score_t4",
    "string_learn_score_l1", "string_learn_score_l2", "string_learn_score_l3", "string_learn_score_l4",
    "string_level_combined",
    "string_comm_score_c1", "string_comm_score_c2", "string_comm_score_c3", "string_comm_score_c4",
    "string_summary_t", "string_summary_l", "string_summary_c",
    "string_total_score", "string_help_status", "string_coding_level", "string_review_comments",

    # Core OOP Principles (35 cols: indices 41-75)
    "oop_class_practice", "oop_lab_practice", "oop_assignment",
    "oop_tech_input_t1", "oop_tech_input_t2", "oop_tech_input_t3", "oop_tech_input_t4",
    "oop_learn_input_l1", "oop_learn_input_l2", "oop_learn_input_l3", "oop_learn_input_l4",
    "oop_comm_input_c1", "oop_comm_input_c2", "oop_comm_input_c3", "oop_comm_input_c4",
    "oop_tech_score_t1", "oop_tech_score_t2", "oop_tech_score_t3", "oop_tech_score_t4",
    "oop_learn_score_l1", "oop_learn_score_l2", "oop_learn_score_l3", "oop_learn_score_l4",
    "oop_level_combined",
    "oop_comm_score_c1", "oop_comm_score_c2", "oop_comm_score_c3", "oop_comm_score_c4",
    "oop_summary_t", "oop_summary_l", "oop_summary_c",
    "oop_total_score", "oop_help_status", "oop_coding_level", "oop_review_comments",

    # Advanced OOP Concepts and Data Structure (35 cols: indices 76-110)
    "adv_oop_class_practice", "adv_oop_lab_practice", "adv_oop_assignment",
    "adv_oop_tech_input_t1", "adv_oop_tech_input_t2", "adv_oop_tech_input_t3", "adv_oop_tech_input_t4",
    "adv_oop_learn_input_l1", "adv_oop_learn_input_l2", "adv_oop_learn_input_l3", "adv_oop_learn_input_l4",
    "adv_oop_comm_input_c1", "adv_oop_comm_input_c2", "adv_oop_comm_input_c3", "adv_oop_comm_input_c4",
    "adv_oop_tech_score_t1", "adv_oop_tech_score_t2", "adv_oop_tech_score_t3", "adv_oop_tech_score_t4",
    "adv_oop_learn_score_l1", "adv_oop_learn_score_l2", "adv_oop_learn_score_l3", "adv_oop_learn_score_l4",
    "adv_oop_level_combined",
    "adv_oop_comm_score_c1", "adv_oop_comm_score_c2", "adv_oop_comm_score_c3", "adv_oop_comm_score_c4",
    "adv_oop_summary_t", "adv_oop_summary_l", "adv_oop_summary_c",
    "adv_oop_total_score", "adv_oop_help_status", "adv_oop_coding_level", "adv_oop_review_comments",

    # Final Tracks (4 cols: indices 111-114)
    "string_final", "oop_final", "adv_oop_final", "final_avg_track",
]

# Build positional index map: col_index (0-based) -> db_column_name
SEM3_INDEX_MAP = {i: col for i, col in enumerate(SEM3_COLUMNS)}


class Semester3Mapping(SemesterMapping):
    HEADER_ROWS = 2

    def extract_core_fields(self, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None]:
        """Extract (student_id, name, email) from positional indices."""
        student_id = None
        name = None
        email = None

        # Col 1 (index 1) = ID
        if len(row_list) > 1:
            val = row_list[1][1]
            student_id = str(val).strip() if val is not None else None

        # Col 2 (index 2) = Full Name
        if len(row_list) > 2:
            val = row_list[2][1]
            name = str(val).strip() if val is not None else None

        # Col 3 (index 3) = College Email ID
        if len(row_list) > 3:
            val = row_list[3][1]
            email = str(val).strip() if val is not None else None

        return student_id, name, email

    def build_record(self, sheet_name: str, row_dict: dict, row_list: list,
                     student_id: str, name: str, email: str) -> dict:
        """Build a flat record dict using positional column mapping."""
        record = {col: None for col in SEM3_COLUMNS}

        for idx, ((top_h, bot_h), val) in enumerate(row_list):
            db_col = SEM3_INDEX_MAP.get(idx)
            if db_col:
                record[db_col] = val

        # Override core fields from extract_core_fields
        record["id"] = student_id
        record["full_name"] = name
        record["college_email_id"] = email

        return record

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        return self.build_record(sheet_name, row_dict, row_list, "", "", "")
