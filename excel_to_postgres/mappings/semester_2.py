import re
import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

SUBJECT_KEYS_SEM2 = [
    ("programming construct", "programming_construct"),
    ("control flow", "control_flow"),
    ("arrays", "arrays"),
    ("methods", "methods"),
    ("strings", "strings"),
]

def create_empty_sem2_schema(sheet_name: str) -> dict:
    subjects = {}
    subject_scores = {}

    for _, subj_key in SUBJECT_KEYS_SEM2:
        subjects[subj_key] = {
            "levels": None,
            "review": None,
            "learnability": None,
            "technicality": None,
            "communicability": None,
            "review_comment": None,
            "coding_level": None,
        }
        subject_scores[subj_key] = {
            "score_levels": None,
            "score_review": None,
            "score_learnability": None,
            "score_technicality": None,
            "score_communicability": None,
            "score_total": None,
        }

    return {
        "batch": sheet_name,
        "sn": None,
        "gmail_id": None,
        "num_reviews": None,
        "regularity_attendance": None,
        "assignment_submission": None,
        "subjects": subjects,
        "subject_scores": subject_scores,
        "track_results": {
            "programming_construct_control_flow": {
                "average": None,
                "last": None
            },
            "arrays_methods": {
                "average": None,
                "last": None
            },
            "final_average": {
                "average": None,
                "last": None
            }
        }
    }

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
            if not email and ("srm email id" in combined or ("email" in combined and "gmail" not in combined)):
                email = str(val) if val is not None else None

        return student_id, name, email

    def _match_subject_key(self, text: str) -> str | None:
        text_norm = self._normalize(text)
        for keyword, key in SUBJECT_KEYS_SEM2:
            if keyword in text_norm:
                return key
        return None

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        data = create_empty_sem2_schema(sheet_name)

        for (top, bot), val in row_dict.items():
            top_n = self._normalize(top)
            bot_n = self._normalize(bot)
            combined = f"{top_n} {bot_n}".strip()

            if top_n == "sn" or bot_n == "sn" or combined == "sn":
                data["sn"] = val
                continue
            elif "# of reviews" in combined or "number of reviews" in combined or "num_reviews" in combined:
                data["num_reviews"] = val
                continue
            elif "regularity attendance" in combined or "attendance" in combined:
                data["regularity_attendance"] = val
                continue
            elif "assignment submission" in combined:
                data["assignment_submission"] = val
                continue
            elif "gmail id" in combined or "gmail" in combined:
                data["gmail_id"] = val
                continue

            # Track results matching
            if "programming construct and control flow" in combined or "programming construct + control flow" in combined:
                if "average" in combined:
                    data["track_results"]["programming_construct_control_flow"]["average"] = val
                elif "last" in combined:
                    data["track_results"]["programming_construct_control_flow"]["last"] = val
                else:
                    data["track_results"]["programming_construct_control_flow"]["average"] = val
                continue

            if "arrays and method" in combined or "arrays + methods" in combined:
                if "average" in combined:
                    data["track_results"]["arrays_methods"]["average"] = val
                elif "last" in combined:
                    data["track_results"]["arrays_methods"]["last"] = val
                else:
                    data["track_results"]["arrays_methods"]["average"] = val
                continue

            if "final average" in combined:
                if "last" in combined:
                    data["track_results"]["final_average"]["last"] = val
                else:
                    data["track_results"]["final_average"]["average"] = val
                continue

            # Subject / Subject Scores matching
            subj_key = self._match_subject_key(top_n) or self._match_subject_key(bot_n) or self._match_subject_key(combined)
            if subj_key:
                field_target = bot_n if bot_n else top_n

                # Subject evaluation vs score columns
                if "score" in top_n or "score" in bot_n:
                    score_obj = data["subject_scores"][subj_key]
                    if "level" in field_target:
                        score_obj["score_levels"] = val
                    elif "review" in field_target:
                        score_obj["score_review"] = val
                    elif "learnability" in field_target:
                        score_obj["score_learnability"] = val
                    elif "technicality" in field_target:
                        score_obj["score_technicality"] = val
                    elif "communicability" in field_target:
                        score_obj["score_communicability"] = val
                    elif "total" in field_target or "score" in field_target:
                        score_obj["score_total"] = val
                else:
                    subj_obj = data["subjects"][subj_key]
                    if "level" in field_target and "coding" not in field_target:
                        subj_obj["levels"] = val
                    elif "review comment" in field_target or "comment" in field_target:
                        subj_obj["review_comment"] = val
                    elif "review" in field_target:
                        subj_obj["review"] = val
                    elif "learnability" in field_target:
                        subj_obj["learnability"] = val
                    elif "technicality" in field_target:
                        subj_obj["technicality"] = val
                    elif "communicability" in field_target:
                        subj_obj["communicability"] = val
                    elif "coding level" in field_target:
                        subj_obj["coding_level"] = val
                    elif "score" in field_target:
                        data["subject_scores"][subj_key]["score_total"] = val

        return data
