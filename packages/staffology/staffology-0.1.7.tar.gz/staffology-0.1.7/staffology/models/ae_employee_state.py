from enum import Enum


class AeEmployeeState(str, Enum):
    AUTOMATIC = "Automatic"
    OPTOUT = "OptOut"
    OPTIN = "OptIn"
    VOLUNTARYJOINER = "VoluntaryJoiner"
    CONTRACTUALPENSION = "ContractualPension"
    CEASEDMEMBERSHIP = "CeasedMembership"
    LEAVER = "Leaver"
    EXCLUDED = "Excluded"
    ENROL = "Enrol"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)

