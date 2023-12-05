from enum import Enum


class LeaveCalculationType(str, Enum):
    ONETHREESIXTYFIFTHFTE = "OneThreeSixtyFifthFTE"
    ONETHREESIXTYFIFTHPRORATA = "OneThreeSixtyFifthProRata"
    USUALPRORATA = "UsualProRata"
    ONEFIFTHORWORKINGPATTERN = "OneFifthOrWorkingPattern"
    SPECIFYHOURS = "SpecifyHours"

    def __str__(self) -> str:
        return str(self.value)
