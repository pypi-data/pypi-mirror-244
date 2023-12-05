from enum import Enum


class AnnualRoundingRule(str, Enum):
    ROUNDOFF = "RoundOff"
    EXACT = "Exact"
    ROUNDUP = "RoundUp"
    ROUNDDOWN = "RoundDown"

    def __str__(self) -> str:
        return str(self.value)
