import re
import logging
from .base import SemesterMapping

logger = logging.getLogger(__name__)

SUBJECT_KEYS_SEM3 = [
    ("string fundamentals", "string_fundamentals_string_operations_performance_oop_fundamentals"),
    ("core oop principles", "core_oop_principles"),
    ("advanced oop concepts", "advanced_oop_concepts_data_structure"),
]

ASSESSMENT_KEYS = [
    ("class practice", "class_practice"),
    ("lab practice", "lab_practice"),
    ("assignment", "assignment"),
]

CRITERIA_MAP = {
    "t1": "t1",
    "t2": "t2",
    "t3": "t3",
    "t4": "t4",
    "l1": "l1",
    "l2": "l2",
    "l3": "l3",
    "l4": "l4",
    "combined": "combined",
    "c1": "c1",
    "c2": "c2",
    "c3": "c3",
    "c4": "c4",
    "t": "t",
    "l": "l",
    "c": "c",
    "total score": "total_score",
    "total": "total_score",
    "help status": "help_status",
    "coding level": "coding_level",
    "review comments": "review_comments",
    "review comment": "review_comments",
    "comments": "review_comments",
}

def create_empty_assessment_schema() -> dict:
    return {
        "t1": None, "t2": None, "t3": None, "t4": None,
        "l1": None, "l2": None, "l3": None, "l4": None,
        "combined": None,
        "c1": None, "c2": None, "c3": None, "c4": None,
        "t": None, "l": None, "c": None,
        "total_score": None,
        "help_status": None,
        "coding_level": None,
        "review_comments": None
    }

def create_empty_sem3_schema(sheet_name: str) -> dict:
    subjects = {}
    track_results = {}

    for _, subj_key in SUBJECT_KEYS_SEM3:
        subjects[subj_key] = {
            "levels": None,
            "inputs": {
                "tech_excellence_input": None,
                "learnability_input": None,
                "communicability_input": None
            },
            "scores": {
                "tech_excellence_score": None,
                "learnability_score": None,
                "communicability_score": None
            },
            "assessments": {
                "class_practice": None,
                "lab_practice": None,
                "assignment": None
            }
        }
        track_results[f"{subj_key}_final_track"] = None

    track_results["final_average_track"] = None

    return {
        "batch": sheet_name,
        "sn": None,
        "assignment_submission": None,
        "engagement_status": None,
        "subjects": subjects,
        "track_results": track_results
    }

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

    def _match_subject_key(self, text: str) -> str | None:
        text_norm = self._normalize(text)
        for keyword, key in SUBJECT_KEYS_SEM3:
            if keyword in text_norm:
                return key
        return None

    def _match_assessment(self, top_n: str, bot_n: str) -> tuple[str | None, str | None]:
        combined = f"{top_n} {bot_n}".strip()
        for keyword, asm_key in ASSESSMENT_KEYS:
            if keyword in top_n:
                rem = bot_n
                return asm_key, rem
            elif keyword in bot_n:
                rem = bot_n.replace(keyword, "").strip()
                return asm_key, rem if rem else top_n
            elif keyword in combined:
                rem = combined.replace(keyword, "").strip()
                return asm_key, rem
        return None, None

    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        data = create_empty_sem3_schema(sheet_name)

        for (top, bot), val in row_dict.items():
            top_n = self._normalize(top)
            bot_n = self._normalize(bot)
            combined = f"{top_n} {bot_n}".strip()

            if top_n == "sn" or bot_n == "sn" or combined == "sn":
                data["sn"] = val
                continue
            elif "assignment submission" in combined:
                data["assignment_submission"] = val
                continue
            elif "engagement status" in combined:
                data["engagement_status"] = val
                continue
            elif "final average track" in combined:
                data["track_results"]["final_average_track"] = val
                continue
            elif combined in ("id", "full name", "college email id"):
                continue

            # Subject matching
            subj_key = self._match_subject_key(top_n) or self._match_subject_key(bot_n) or self._match_subject_key(combined)
            if not subj_key:
                continue

            subj_obj = data["subjects"][subj_key]

            # Assessment matching
            asm_key, rem_field = self._match_assessment(top_n, bot_n)

            if asm_key:
                if subj_obj["assessments"][asm_key] is None:
                    subj_obj["assessments"][asm_key] = create_empty_assessment_schema()

                rem_clean = rem_field.strip() if rem_field else ""

                if rem_clean in CRITERIA_MAP:
                    crit_key = CRITERIA_MAP[rem_clean]
                    subj_obj["assessments"][asm_key][crit_key] = val
                else:
                    for k, v in CRITERIA_MAP.items():
                        if k == rem_clean or (len(k) > 1 and k in rem_clean):
                            subj_obj["assessments"][asm_key][v] = val
                            break
            else:
                target = bot_n if bot_n else top_n
                
                if "level" in target and "coding" not in target:
                    subj_obj["levels"] = val
                elif "tech excellence input" in target:
                    subj_obj["inputs"]["tech_excellence_input"] = val
                elif "learnability input" in target:
                    subj_obj["inputs"]["learnability_input"] = val
                elif "communicability input" in target:
                    subj_obj["inputs"]["communicability_input"] = val
                elif "tech excellence score" in target:
                    subj_obj["scores"]["tech_excellence_score"] = val
                elif "learnability score" in target:
                    subj_obj["scores"]["learnability_score"] = val
                elif "communicability score" in target:
                    subj_obj["scores"]["communicability_score"] = val
                elif "final track" in target:
                    data["track_results"][f"{subj_key}_final_track"] = val

        return data
