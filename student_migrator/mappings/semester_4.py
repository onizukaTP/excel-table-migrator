import re
import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

SEM4_COLUMNS = [
    "sn", "id", "full_name", "college_email_id", "assignment_submission", "engagement_status",

    "dsa_level", "dsa_class_practice", "dsa_assignment",
    "dsa_tech_input_t1", "dsa_tech_input_t2", "dsa_tech_input_t3", "dsa_tech_input_t4",
    "dsa_learn_input_l1", "dsa_learn_input_l2", "dsa_learn_input_l3", "dsa_learn_input_l4",
    "dsa_comm_input_c1", "dsa_comm_input_c2", "dsa_comm_input_c3", "dsa_comm_input_c4",
    "dsa_tech_score_t1", "dsa_tech_score_t2", "dsa_tech_score_t3", "dsa_tech_score_t4",
    "dsa_learn_score_l1", "dsa_learn_score_l2", "dsa_learn_score_l3", "dsa_learn_score_l4",
    "dsa_learn_score_combined", "dsa_level_computed",
    "dsa_comm_score_c1", "dsa_comm_score_c2", "dsa_comm_score_c3", "dsa_comm_score_c4",
    "dsa_summary_t", "dsa_summary_l", "dsa_summary_c",
    "dsa_total_score", "dsa_help_status", "dsa_coding_level", "dsa_review_comments",

    "collections_level", "collections_class_practice", "collections_assignment",
    "collections_tech_input_t1", "collections_tech_input_t2", "collections_tech_input_t3", "collections_tech_input_t4",
    "collections_learn_input_l1", "collections_learn_input_l2", "collections_learn_input_l3", "collections_learn_input_l4",
    "collections_comm_input_c1", "collections_comm_input_c2", "collections_comm_input_c3", "collections_comm_input_c4",
    "collections_tech_score_t1", "collections_tech_score_t2", "collections_tech_score_t3", "collections_tech_score_t4",
    "collections_learn_score_l1", "collections_learn_score_l2", "collections_learn_score_l3", "collections_learn_score_l4",
    "collections_learn_score_combined", "collections_level_computed",
    "collections_comm_score_c1", "collections_comm_score_c2", "collections_comm_score_c3", "collections_comm_score_c4",
    "collections_summary_t", "collections_summary_l", "collections_summary_c",
    "collections_total_score", "collections_help_status", "collections_coding_level", "collections_review_comments",

    "java_adv_level", "java_adv_class_practice", "java_adv_assignment",
    "java_adv_tech_input_t1", "java_adv_tech_input_t2", "java_adv_tech_input_t3", "java_adv_tech_input_t4",
    "java_adv_learn_input_l1", "java_adv_learn_input_l2", "java_adv_learn_input_l3", "java_adv_learn_input_l4",
    "java_adv_comm_input_c1", "java_adv_comm_input_c2", "java_adv_comm_input_c3", "java_adv_comm_input_c4",
    "java_adv_tech_score_t1", "java_adv_tech_score_t2", "java_adv_tech_score_t3", "java_adv_tech_score_t4",
    "java_adv_learn_score_l1", "java_adv_learn_score_l2", "java_adv_learn_score_l3", "java_adv_learn_score_l4",
    "java_adv_learn_score_combined", "java_adv_level_computed",
    "java_adv_comm_score_c1", "java_adv_comm_score_c2", "java_adv_comm_score_c3", "java_adv_comm_score_c4",
    "java_adv_summary_t", "java_adv_summary_l", "java_adv_summary_c",
    "java_adv_total_score", "java_adv_help_status", "java_adv_coding_level", "java_adv_review_comments",

    "dsa_final", "collections_final", "java_adv_final", "final_avg_track"
]

SUBJECT_PREFIXES_SEM4 = [
    ("data structures and algorithms", "dsa"),
    ("data structures", "dsa"),
    ("collections and stream api", "collections"),
    ("collections", "collections"),
    ("java advanced", "java_adv"),
]

class Semester4Mapping(SemesterMapping):
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
            if not email and ("college email" in combined or "email id" in combined or ("email" in combined and "gmail" not in combined)):
                email = str(val) if val is not None else None

        return student_id, name, email

    def build_record(self, sheet_name: str, row_dict: dict, row_list: list, student_id: str, name: str, email: str) -> dict:
        record = {col: None for col in SEM4_COLUMNS}
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
            elif "final average track" in combined:
                record["final_avg_track"] = val

            # Subject matching
            prefix = None
            for kw, pfx in SUBJECT_PREFIXES_SEM4:
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
                elif "summary" in field_target or field_target in ("t", "l", "c"):
                    if field_target == "t" or "summary t" in field_target: record[f"{prefix}_summary_t"] = val
                    elif field_target == "l" or "summary l" in field_target: record[f"{prefix}_summary_l"] = val
                    elif field_target == "c" or "summary c" in field_target: record[f"{prefix}_summary_c"] = val
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
