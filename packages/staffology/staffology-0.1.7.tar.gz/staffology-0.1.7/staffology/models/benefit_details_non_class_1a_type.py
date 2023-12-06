from enum import Enum


class BenefitDetailsNonClass1AType(str, Enum):
    OTHER = "Other"
    MULTIPLE = "Multiple"
    LOANSWRITTENORWAIVED = "LoansWrittenOrWaived"
    NURSERYPLACES = "NurseryPlaces"
    EDUCATIONALASSITANCE = "EducationalAssitance"
    SUBSCRIPTIONSANDFEES = "SubscriptionsAndFees"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
