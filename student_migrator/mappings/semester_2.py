import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────
# Semester 2 — Positional Column Index Map
# ──────────────────────────────────────────────────────────────────────
# The Sem 2 Excel has 78 columns with 2 header rows.
# Col indices are 0-based (matching row_list position).
#
# Sem 2 structure is DIFFERENT from Sem 3/4:
#   - 5 subjects: Programming Construct, Control Flow, Arrays, Methods, Strings
#   - Each subject has 7 INPUT fields: Levels, Review, Learnability,
#     Technicality, Communicability, Review Comment, Coding Level
#   - Each subject has 6 SCORE fields: Levels, Review, Learnability,
#     Technicality, Communicability, Total
#   - Final tracks: PC+CF Average/Last, Arrays+Methods Average/Last, Final Average
# ──────────────────────────────────────────────────────────────────────

# DB column names in positional order (0-indexed matching Excel columns)
SEM2_COLUMNS = [
    "sn", "id", "full_name", "college_email_id", "gmail_id",
    "num_reviews", "regularity_attendance", "assignment_submission",

    # Programming Construct — Input (7 cols)
    "prog_level", "prog_review", "prog_learnability", "prog_technicality",
    "prog_communicability", "prog_review_comment", "prog_coding_level",

    # Control Flow — Input (7 cols)
    "cf_level", "cf_review", "cf_learnability", "cf_technicality",
    "cf_communicability", "cf_review_comment", "cf_coding_level",

    # Arrays — Input (7 cols)
    "arr_level", "arr_review", "arr_learnability", "arr_technicality",
    "arr_communicability", "arr_review_comment", "arr_coding_level",

    # Methods — Input (7 cols)
    "meth_level", "meth_review", "meth_learnability", "meth_technicality",
    "meth_communicability", "meth_review_comment", "meth_coding_level",

    # Strings — Input (7 cols)
    "str_level", "str_review", "str_learnability", "str_technicality",
    "str_communicability", "str_review_comment", "str_coding_level",

    # Programming Construct — Score (6 cols)
    "prog_score_level", "prog_score_review", "prog_score_learnability",
    "prog_score_technicality", "prog_score_communicability", "prog_score_total",

    # Control Flow — Score (6 cols)
    "cf_score_level", "cf_score_review", "cf_score_learnability",
    "cf_score_technicality", "cf_score_communicability", "cf_score_total",

    # Arrays — Score (6 cols)
    "arr_score_level", "arr_score_review", "arr_score_learnability",
    "arr_score_technicality", "arr_score_communicability", "arr_score_total",

    # Methods — Score (6 cols)
    "meth_score_level", "meth_score_review", "meth_score_learnability",
    "meth_score_technicality", "meth_score_communicability", "meth_score_total",

    # Strings — Score (6 cols)
    "str_score_level", "str_score_review", "str_score_learnability",
    "str_score_technicality", "str_score_communicability", "str_score_total",

    # Final Tracks (5 cols)
    "prog_cf_final_avg", "prog_cf_final_last",
    "arr_meth_final_avg", "arr_meth_final_last",
    "final_average",
]

# Build positional index map: col_index (0-based) -> db_column_name
SEM2_INDEX_MAP = {i: col for i, col in enumerate(SEM2_COLUMNS)}


class Semester2Mapping(SemesterMapping):
    HEADER_ROWS = 2

    def extract_core_fields(self, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None]:
        """Extract (student_id, name, email) from positional indices."""
        student_id = None
        name = None
        email = None

        # Col 1 (index 1) = Register number / ID
        if len(row_list) > 1:
            val = row_list[1][1]
            student_id = str(val).strip() if val is not None else None

        # Col 2 (index 2) = Full Name
        if len(row_list) > 2:
            val = row_list[2][1]
            name = str(val).strip() if val is not None else None

        # Col 3 (index 3) = SRM Email ID
        if len(row_list) > 3:
            val = row_list[3][1]
            email = str(val).strip() if val is not None else None

        return student_id, name, email

    def build_record(self, sheet_name: str, row_dict: dict, row_list: list,
                     student_id: str, name: str, email: str) -> dict:
        """Build a flat record dict using positional column mapping."""
        record = {col: None for col in SEM2_COLUMNS}

        for idx, ((top_h, bot_h), val) in enumerate(row_list):
            db_col = SEM2_INDEX_MAP.get(idx)
            if db_col:
                record[db_col] = val

        # Override core fields from extract_core_fields (ensures consistent ID/name/email)
        record["id"] = student_id
        record["full_name"] = name
        record["college_email_id"] = email

        return record

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        return self.build_record(sheet_name, row_dict, row_list, "", "", "")
