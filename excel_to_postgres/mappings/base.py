from abc import ABC, abstractmethod

class SemesterMapping(ABC):
    HEADER_ROWS: int = 2

    @abstractmethod
    def extract_core_fields(self, row_dict: dict, row_list: list) -> tuple[str | None, str | None, str | None]:
        """Returns (student_id, name, email)."""
        pass

    @abstractmethod
    def build_json(self, sheet_name: str, row_dict: dict, row_list: list) -> dict:
        """Returns the JSON payload for the specific semester's table."""
        pass
