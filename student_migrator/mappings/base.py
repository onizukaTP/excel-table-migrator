from abc import ABC, abstractmethod

class SemesterMapping(ABC):
    HEADER_ROWS: int = 2

    @abstractmethod
    def extract_core_fields(self, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None]:
        """Returns (student_id, name, email)."""
        pass

    @abstractmethod
    def build_record(self, sheet_name: str, row_dict: dict, row_list: list, student_id: str, name: str, email: str) -> dict:
        """Returns the flat record payload dictionary for the specific semester's MySQL table."""
        pass
