from enum import Enum


class WebhookEvent(str, Enum):
    EMPLOYEE_CREATED = "Employee_Created"
    EMPLOYEE_UPDATED = "Employee_Updated"
    EMPLOYEE_DELETED = "Employee_Deleted"
    PAYRUN_FINALISED = "Payrun_Finalised"
    PAYRUN_STATECHANGED = "Payrun_StateChanged"
    PENSIONMEMBERSHIP_CREATED = "PensionMembership_Created"
    PENSIONMEMBERSHIP_UPDATED = "PensionMembership_Updated"
    PENSIONMEMBERSHIP_DELETED = "PensionMembership_Deleted"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)