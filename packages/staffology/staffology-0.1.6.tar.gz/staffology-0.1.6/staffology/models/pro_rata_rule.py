from enum import Enum


class ProRataRule(str, Enum):
    WORKINGDAYSINPERIOD = "WorkingDaysInPeriod"
    CALENDARDAYSINPERIOD = "CalendarDaysInPeriod"
    TWOSIXTYRULE = "TwoSixtyRule"
    THREESIXFIVERULE = "ThreeSixFiveRule"

    def __str__(self) -> str:
        return str(self.value)
