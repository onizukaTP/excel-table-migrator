import re
import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

SEM3_COLUMNS = [
    "sn", "id", "full_name", "college_email_id", "assignment_submission", "engagement_status",

    "string_level", "string_class_practice", "string_assignment",
    "string_tech_input_t1", "string_tech_input_t2", "string_tech_input_t3", "string_tech_input_t4",
    "string_learn_input_l1", "string_learn_input_l2", "string_learn_input_l3", "string_learn_input_l4",
    "string_comm_input_c1", "string_comm_input_c2", "string_comm_input_c3", "string_comm_input_c4",
    "string_tech_score_t1", "string_tech_score_t2", "string_tech_score_t3", "string_tech_score_t4",
    "string_learn_score_l1", "string_learn_score_l2", "string_learn_score_l3", "string_learn_score_l4",
    "string_learn_score_combined", "string_level_computed",
    "string_comm_score_c1", "string_comm_score_c2", "string_comm_score_c3", "string_comm_score_c4",
    "string_summary_t", "string_summary_l", "string_summary_c",
    "string_total_score", "string_help_status", "string_coding_level", "string_review_comments",

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

    "adv_oop_level", "adv_oop_class_practice", "adv_oop_assignment",
    "adv_oop_tech_input_t1", "adv_oop_tech_input_t2", "adv_oop_tech_input_t3", "adv_oop_tech_input_t4",
    "adv_oop_learn_input_l1", "adv_oop_learn_input_l2", "adv_oop_learn_input_l3", "adv_oop_learn_input_l4",
    "adv_oop_comm_input_c1", "adv_oop_comm_input_c2", "adv_oop_comm_input_c3", "adv_oop_comm_input_c4",
    "adv_oop_tech_score_t1", "adv_oop_tech_score_t2", "adv_oop_tech_score_t3", "adv_oop_tech_score_t4",
    "adv_oop_learn_score_l1", "adv_oop_learn_score_l2", "adv_oop_learn_score_l3", "adv_oop_learn_score_l4",
    "adv_oop_learn_score_combined", "adv_oop_level_computed",
    "adv_oop_comm_score_c1", "adv_oop_comm_score_c2", "adv_oop_comm_score_c3", "adv_oop_comm_score_c4",
    "adv_oop_summary_t", "adv_oop_summary_l", "adv_oop_summary_c",
    "adv_oop_total_score", "adv_oop_help_status", "adv_oop_coding_level", "adv_oop_review_comments",

    "string_final", "oop_final", "adv_oop_final", "final_avg_track"
]

SUBJECT_PREFIXES_SEM3 = [
    ("string fundamentals", "string"),
    ("core oop principles", "oop"),
    ("advanced oop concepts", "adv_oop"),
]

class Semester3Mapping(SemesterMapping):
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
        record = {col: None for col in SEM3_COLUMNS}
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
            for kw, pfx in SUBJECT_PREFIXES_SEM3:
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
