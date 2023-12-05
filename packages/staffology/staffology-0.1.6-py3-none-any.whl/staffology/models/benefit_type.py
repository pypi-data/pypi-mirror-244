from enum import Enum


class BenefitType(str, Enum):
    ASSETSTRANSFERRED = "AssetsTransferred"
    PAYMENTSONBEHALF = "PaymentsOnBehalf"
    UNBORNETAX = "UnborneTax"
    VOUCHERS = "Vouchers"
    ACCOMMODATION = "Accommodation"
    MILEAGEALLOWANCE = "MileageAllowance"
    CAR = "Car"
    VANS = "Vans"
    LOAN = "Loan"
    MEDICAL = "Medical"
    QUALIFYINGRELOCATIONEXPENSES = "QualifyingRelocationExpenses"
    SERVICES = "Services"
    ASSETSATEMPLOYEEDISPOSAL = "AssetsAtEmployeeDisposal"
    OTHERCLASS1AITEMS = "OtherClass1AItems"
    OTHERNONCLASS1AITEMS = "OtherNonClass1AItems"
    DIRECTORTAX = "DirectorTax"
    TRAVELLINGANDSUBSISTENCE = "TravellingAndSubsistence"
    ENTERTAINMENT = "Entertainment"
    HOMETELEPHONE = "HomeTelephone"
    NONQUALIFYINGRELOCATIONEXPENSES = "NonQualifyingRelocationExpenses"
    OTHEREXPENSES = "OtherExpenses"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
