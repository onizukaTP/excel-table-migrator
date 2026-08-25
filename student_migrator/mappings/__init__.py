from .semester_2 import Semester2Mapping
from .semester_3 import Semester3Mapping
from .semester_4 import Semester4Mapping

def get_mapping(semester: int):
    if semester == 2:
        return Semester2Mapping()
    elif semester == 3:
        return Semester3Mapping()
    elif semester == 4:
        return Semester4Mapping()
    else:
        raise ValueError(f"Unsupported semester: {semester}")
