import re
import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

SEM2_COLUMNS = [
    "sn", "id", "full_name", "college_email_id", "assignment_submission", "engagement_status",
    "core_level", "core_class_practice", "core_assignment",
    "core_tech_input_t1", "core_tech_input_t2", "core_tech_input_t3", "core_tech_input_t4",
    "core_learn_input_l1", "core_learn_input_l2", "core_learn_input_l3", "core_learn_input_l4",
    "core_comm_input_c1", "core_comm_input_c2", "core_comm_input_c3", "core_comm_input_c4",
    "core_tech_score_t1", "core_tech_score_t2", "core_tech_score_t3", "core_tech_score_t4",
    "core_learn_score_l1", "core_learn_score_l2", "core_learn_score_l3", "core_learn_score_l4",
    "core_learn_score_combined", "core_level_computed",
    "core_comm_score_c1", "core_comm_score_c2", "core_comm_score_c3", "core_comm_score_c4",
    "core_summary_t", "core_summary_l", "core_summary_c",
    "core_total_score", "core_help_status", "core_coding_level", "core_review_comments",

    "logical_level", "logical_class_practice", "logical_assignment",
    "logical_tech_input_t1", "logical_tech_input_t2", "logical_tech_input_t3", "logical_tech_input_t4",
    "logical_learn_input_l1", "logical_learn_input_l2", "logical_learn_input_l3", "logical_learn_input_l4",
    "logical_comm_input_c1", "logical_comm_input_c2", "logical_comm_input_c3", "logical_comm_input_c4",
    "logical_tech_score_t1", "logical_tech_score_t2", "logical_tech_score_t3", "logical_tech_score_t4",
    "logical_learn_score_l1", "logical_learn_score_l2", "logical_learn_score_l3", "logical_learn_score_l4",
    "logical_learn_score_combined", "logical_level_computed",
    "logical_comm_score_c1", "logical_comm_score_c2", "logical_comm_score_c3", "logical_comm_score_c4",
    "logical_summary_t", "logical_summary_l", "logical_summary_c",
    "logical_total_score", "logical_help_status", "logical_coding_level", "logical_review_comments",

    "oop_level", "oop_class_practice", "oop_assignment",
    "oop_tech_input_t1", "oop_tech_input_t2", "oop_tech_input_t3", "oop_tech_input_t4",
    "oop_learn_input_l1", "oop_learn_input_l2", "oop_learn_input_l3", "oop_learn_input_l4",
    "oop_comm_input_c1", "oop_comm_input_c2", "oop_comm_input_c3", "oop_comm_input_c4",
    "oop_tech_score_t1", "oop_tech_score_t2", "oop_tech_score_t3", "oop_tech_score_t4",
    "oop_learn_score_l1", "oop_learn_score_l2", "oop_learn_score_l3", "oop_learn_score_l4",
    "oop_learn_score_combined", "oop_level_computed",
    "oop_comm_score_c1", "oop_comm_score_c2", "oop_comm_score_c3", "oop_comm_score_c4",
    "oop_summary_t", "oop_summary_l", "oop_summary_c",
    "oop_total_score", "oop_help_status", "oop_coding_level", "oop_review_comments",

    "core_final", "logical_final", "oop_final", "final_avg_track"
]

SUBJECT_PREFIXES_SEM2 = [
    ("programming construct", "core"),
    ("control flow", "logical"),
    ("arrays", "oop"),
    ("methods", "oop"),
    ("strings", "oop"),
]

class Semester2Mapping(SemesterMapping):
    HEADER_ROWS = 2

    def _normalize(self, s: str) -> str:
        return s.strip().lower() if s else ""

    def extract_core_fields(self, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None]:
        student_id = None
        name = None
        email = None

        id_keywords = (
            "register number", "reg number", "reg no", "reg.no", "reg_no",
            "registration number", "student id", "student_id", "roll no", "roll number",
            "id", "id no", "id_no"
        )

        for (top, bot), val in row_dict.items():
            top_n = self._normalize(top)
            bot_n = self._normalize(bot)
            combined = f"{top_n} {bot_n}".strip()

            if top_n in ("sn", "s.no", "sno") or bot_n in ("sn", "s.no", "sno"):
                continue

            if not student_id:
                if top_n in id_keywords or bot_n in id_keywords or combined in id_keywords or "register number" in combined or "registration number" in combined:
                    student_id = str(val) if val is not None else None
            if not name and ("full name" in combined or "student name" in combined or top_n == "name" or bot_n == "name" or combined == "name"):
                name = str(val) if val is not None else None
            if not email and ("srm email id" in combined or "college email" in combined or ("email" in combined and "gmail" not in combined)):
                email = str(val) if val is not None else None

        return student_id, name, email

    def build_record(self, sheet_name: str, row_dict: dict, row_list: list, student_id: str, name: str, email: str) -> dict:
        record = {col: None for col in SEM2_COLUMNS}
        record["id"] = student_id
        record["full_name"] = name
        record["college_email_id"] = email

        for (top, bot), val in row_dict.items():
            top_n = self._normalize(top)
            bot_n = self._normalize(bot)
            combined = f"{top_n} {bot_n}".strip()

            if top_n == "sn" or bot_n == "sn" or combined == "sn":
                record["sn"] = val
            elif "assignment submission" in combined:
                record["assignment_submission"] = val
            elif "engagement status" in combined:
                record["engagement_status"] = val
            elif "final average track" in combined or ("final average" in combined and "track" in combined):
                record["final_avg_track"] = val

            # Subject matching
            prefix = None
            for kw, pfx in SUBJECT_PREFIXES_SEM2:
                if kw in top_n or kw in combined:
                    prefix = pfx
                    break

            if prefix:
                field_target = bot_n if bot_n else top_n
                if "level" in field_target and "coding" not in field_target and "computed" not in field_target:
                    record[f"{prefix}_level"] = val
                elif "class practice" in field_target:
                    record[f"{prefix}_class_practice"] = val
                elif "assignment" in field_target:
                    record[f"{prefix}_assignment"] = val
                elif "tech" in field_target and "input" in field_target:
                    if "t1" in field_target: record[f"{prefix}_tech_input_t1"] = val
                    elif "t2" in field_target: record[f"{prefix}_tech_input_t2"] = val
                    elif "t3" in field_target: record[f"{prefix}_tech_input_t3"] = val
                    elif "t4" in field_target: record[f"{prefix}_tech_input_t4"] = val
                elif "learn" in field_target and "input" in field_target:
                    if "l1" in field_target: record[f"{prefix}_learn_input_l1"] = val
                    elif "l2" in field_target: record[f"{prefix}_learn_input_l2"] = val
                    elif "l3" in field_target: record[f"{prefix}_learn_input_l3"] = val
                    elif "l4" in field_target: record[f"{prefix}_learn_input_l4"] = val
                elif "comm" in field_target and "input" in field_target:
                    if "c1" in field_target: record[f"{prefix}_comm_input_c1"] = val
                    elif "c2" in field_target: record[f"{prefix}_comm_input_c2"] = val
                    elif "c3" in field_target: record[f"{prefix}_comm_input_c3"] = val
                    elif "c4" in field_target: record[f"{prefix}_comm_input_c4"] = val
                elif "tech" in field_target and "score" in field_target:
                    if "t1" in field_target: record[f"{prefix}_tech_score_t1"] = val
                    elif "t2" in field_target: record[f"{prefix}_tech_score_t2"] = val
                    elif "t3" in field_target: record[f"{prefix}_tech_score_t3"] = val
                    elif "t4" in field_target: record[f"{prefix}_tech_score_t4"] = val
                elif "learn" in field_target and "score" in field_target:
                    if "l1" in field_target: record[f"{prefix}_learn_score_l1"] = val
                    elif "l2" in field_target: record[f"{prefix}_learn_score_l2"] = val
                    elif "l3" in field_target: record[f"{prefix}_learn_score_l3"] = val
                    elif "l4" in field_target: record[f"{prefix}_learn_score_l4"] = val
                    elif "combined" in field_target: record[f"{prefix}_learn_score_combined"] = val
                elif "comm" in field_target and "score" in field_target:
                    if "c1" in field_target: record[f"{prefix}_comm_score_c1"] = val
                    elif "c2" in field_target: record[f"{prefix}_comm_score_c2"] = val
                    elif "c3" in field_target: record[f"{prefix}_comm_score_c3"] = val
                    elif "c4" in field_target: record[f"{prefix}_comm_score_c4"] = val
                elif "summary" in field_target:
                    if "t" in field_target: record[f"{prefix}_summary_t"] = val
                    elif "l" in field_target: record[f"{prefix}_summary_l"] = val
                    elif "c" in field_target: record[f"{prefix}_summary_c"] = val
                elif "total" in field_target or "score" in field_target:
                    record[f"{prefix}_total_score"] = val
                elif "help" in field_target:
                    record[f"{prefix}_help_status"] = val
                elif "coding level" in field_target:
                    record[f"{prefix}_coding_level"] = val
                elif "comment" in field_target or "review" in field_target:
                    record[f"{prefix}_review_comments"] = val
                elif "final" in field_target or "track" in field_target:
                    record[f"{prefix}_final"] = val

        return record

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        return self.build_record(sheet_name, row_dict, row_list, "", "", "")
