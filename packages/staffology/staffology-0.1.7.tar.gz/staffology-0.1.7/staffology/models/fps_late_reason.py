from enum import Enum


class FpsLateReason(str, Enum):
    NONEGIVEN = "NoneGiven"
    NOTIONALEXPAT = "NotionalExpat"
    NOTIONALERS = "NotionalErs"
    NOTIONALOTHER = "NotionalOther"
    CLASS1 = "Class1"
    MICROEMPLOYER = "MicroEmployer"
    NOREQUIREMENT = "NoRequirement"
    REASONABLEEXCUSE = "ReasonableExcuse"
    CORRECTION = "Correction"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
