from enum import Enum


class HoursNormallyWorked(str, Enum):
    LESSTHAN16 = "LessThan16"
    MORETHAN16 = "MoreThan16"
    MORETHAN24 = "MoreThan24"
    MORETHAN30 = "MoreThan30"
    NOTREGULAR = "NotRegular"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
