from enum import Enum


class Country(str, Enum):
    ENGLAND = "England"
    NORTHERNIRELAND = "NorthernIreland"
    SCOTLAND = "Scotland"
    WALES = "Wales"
    OUTSIDEUK = "OutsideUk"
    UK = "Uk"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
