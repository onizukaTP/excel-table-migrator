import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────
# Semester 4 — Positional Column Index Map
# ──────────────────────────────────────────────────────────────────────
# The Sem 4 Excel has 114 data columns (cols 115-119 are empty padding).
# Col indices are 0-based (matching row_list position).
#
# 3 subjects with 35 columns each:
#   - Data Structures and Algorithms
#   - Collections and Stream API
#   - Java Advanced
#
# Each subject block (35 cols):
#   class_practice, lab_practice, assignment,
#   tech_input t1-t4, learn_input l1-l4, comm_input c1-c4,
#   tech_score t1-t4, learn_score l1-l4, level_combined,
#   comm_score c1-c4, summary_t, summary_l, summary_c,
#   total_score, help_status, coding_level, review_comments
# ──────────────────────────────────────────────────────────────────────

SEM4_COLUMNS = [
    # Common (6 cols: indices 0-5)
    "sn", "id", "full_name", "college_email_id", "assignment_submission", "engagement_status",

    # Data Structures and Algorithms (35 cols: indices 6-40)
    "dsa_class_practice", "dsa_lab_practice", "dsa_assignment",
    "dsa_tech_input_t1", "dsa_tech_input_t2", "dsa_tech_input_t3", "dsa_tech_input_t4",
    "dsa_learn_input_l1", "dsa_learn_input_l2", "dsa_learn_input_l3", "dsa_learn_input_l4",
    "dsa_comm_input_c1", "dsa_comm_input_c2", "dsa_comm_input_c3", "dsa_comm_input_c4",
    "dsa_tech_score_t1", "dsa_tech_score_t2", "dsa_tech_score_t3", "dsa_tech_score_t4",
    "dsa_learn_score_l1", "dsa_learn_score_l2", "dsa_learn_score_l3", "dsa_learn_score_l4",
    "dsa_level_combined",
    "dsa_comm_score_c1", "dsa_comm_score_c2", "dsa_comm_score_c3", "dsa_comm_score_c4",
    "dsa_summary_t", "dsa_summary_l", "dsa_summary_c",
    "dsa_total_score", "dsa_help_status", "dsa_coding_level", "dsa_review_comments",

    # Collections and Stream API (35 cols: indices 41-75)
    "collections_class_practice", "collections_lab_practice", "collections_assignment",
    "collections_tech_input_t1", "collections_tech_input_t2", "collections_tech_input_t3", "collections_tech_input_t4",
    "collections_learn_input_l1", "collections_learn_input_l2", "collections_learn_input_l3", "collections_learn_input_l4",
    "collections_comm_input_c1", "collections_comm_input_c2", "collections_comm_input_c3", "collections_comm_input_c4",
    "collections_tech_score_t1", "collections_tech_score_t2", "collections_tech_score_t3", "collections_tech_score_t4",
    "collections_learn_score_l1", "collections_learn_score_l2", "collections_learn_score_l3", "collections_learn_score_l4",
    "collections_level_combined",
    "collections_comm_score_c1", "collections_comm_score_c2", "collections_comm_score_c3", "collections_comm_score_c4",
    "collections_summary_t", "collections_summary_l", "collections_summary_c",
    "collections_total_score", "collections_help_status", "collections_coding_level", "collections_review_comments",

    # Java Advanced (35 cols: indices 76-110)
    "java_adv_class_practice", "java_adv_lab_practice", "java_adv_assignment",
    "java_adv_tech_input_t1", "java_adv_tech_input_t2", "java_adv_tech_input_t3", "java_adv_tech_input_t4",
    "java_adv_learn_input_l1", "java_adv_learn_input_l2", "java_adv_learn_input_l3", "java_adv_learn_input_l4",
    "java_adv_comm_input_c1", "java_adv_comm_input_c2", "java_adv_comm_input_c3", "java_adv_comm_input_c4",
    "java_adv_tech_score_t1", "java_adv_tech_score_t2", "java_adv_tech_score_t3", "java_adv_tech_score_t4",
    "java_adv_learn_score_l1", "java_adv_learn_score_l2", "java_adv_learn_score_l3", "java_adv_learn_score_l4",
    "java_adv_level_combined",
    "java_adv_comm_score_c1", "java_adv_comm_score_c2", "java_adv_comm_score_c3", "java_adv_comm_score_c4",
    "java_adv_summary_t", "java_adv_summary_l", "java_adv_summary_c",
    "java_adv_total_score", "java_adv_help_status", "java_adv_coding_level", "java_adv_review_comments",

    # Final Tracks (4 cols: indices 111-114)
    "dsa_final", "collections_final", "java_adv_final", "final_avg_track",
]

# Build positional index map: col_index (0-based) -> db_column_name
SEM4_INDEX_MAP = {i: col for i, col in enumerate(SEM4_COLUMNS)}


class Semester4Mapping(SemesterMapping):
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
        record = {col: None for col in SEM4_COLUMNS}

        for idx, ((top_h, bot_h), val) in enumerate(row_list):
            db_col = SEM4_INDEX_MAP.get(idx)
            if db_col:
                record[db_col] = val

        # Override core fields from extract_core_fields
        record["id"] = student_id
        record["full_name"] = name
        record["college_email_id"] = email

        return record

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        return self.build_record(sheet_name, row_dict, row_list, "", "", "")
