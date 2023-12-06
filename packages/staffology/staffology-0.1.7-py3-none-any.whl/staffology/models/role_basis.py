from enum import Enum


class RoleBasis(str, Enum):
    NOTAPPLICABLE = "NotApplicable"
    PERMANENT = "Permanent"
    TEMPORARY = "Temporary"
    FIXEDTERM = "FixedTerm"
    ZEROHOURS = "ZeroHours"
    CASUAL = "Casual"
    SUPPLY = "Supply"

    def __str__(self) -> str:
        return str(self.value)
