from enum import Enum


class LeavePayType(str, Enum):
    DONOTPAY = "DoNotPay"
    PAYASUSUAL = "PayAsUsual"
    STATUTORYPAY = "StatutoryPay"
    OCCUPATIONALPOLICY = "OccupationalPolicy"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
