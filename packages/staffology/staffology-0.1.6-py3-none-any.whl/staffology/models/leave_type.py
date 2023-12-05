from enum import Enum


class LeaveType(str, Enum):
    UNAUTHORISED = "Unauthorised"
    HOLIDAY = "Holiday"
    SICK = "Sick"
    MATERNITY = "Maternity"
    PATERNITY = "Paternity"
    ADOPTION = "Adoption"
    SHAREDPARENTAL = "SharedParental"
    BEREAVEMENT = "Bereavement"
    SHAREDPARENTALADOPTION = "SharedParentalAdoption"
    PATERNITYADOPTION = "PaternityAdoption"
    STRIKEACTION = "StrikeAction"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)