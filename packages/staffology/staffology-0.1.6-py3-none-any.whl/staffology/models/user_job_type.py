from enum import Enum


class UserJobType(str, Enum):
    BUSINESSOWNER = "BusinessOwner"
    PAYROLLMANAGER = "PayrollManager"
    ACCOUNTANT = "Accountant"
    DEVELOPER = "Developer"
    SOFTWAREVENDOR = "SoftwareVendor"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)