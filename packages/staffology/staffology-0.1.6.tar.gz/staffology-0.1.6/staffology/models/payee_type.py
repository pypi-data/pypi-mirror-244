from enum import Enum


class PayeeType(str, Enum):
    EMPLOYEE = "Employee"
    HMRC = "Hmrc"
    PENSIONPROVIDER = "PensionProvider"
    AEO = "Aeo"
    DEDUCTION = "Deduction"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)