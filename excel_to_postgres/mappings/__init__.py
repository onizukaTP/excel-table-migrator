"""
Semester Mappings Package
"""
from .semester_2 import Semester2Mapping
from .semester_3 import Semester3Mapping
from .semester_4 import Semester4Mapping

MAPPINGS = {
    2: Semester2Mapping,
    3: Semester3Mapping,
    4: Semester4Mapping,
}

def get_mapping(semester: int):
    mapping_cls = MAPPINGS.get(semester)
    if not mapping_cls:
        raise ValueError(f"No mapping defined for semester {semester}. Supported semesters: {list(MAPPINGS.keys())}")
    return mapping_cls()
