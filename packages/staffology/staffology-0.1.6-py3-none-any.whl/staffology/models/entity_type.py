from enum import Enum


class EntityType(str, Enum):
    NONE = "None"
    EMPLOYER = "Employer"
    EMPLOYEE = "Employee"
    PAYRUNENTRY = "PayRunEntry"
    PENSIONSCHEME = "PensionScheme"
    PAYCODE = "PayCode"
    NOTE = "Note"
    LEAVE = "Leave"
    BENEFITS = "Benefits"
    PENSION = "Pension"
    ATTACHMENTORDER = "AttachmentOrder"
    OPENINGBALANCES = "OpeningBalances"
    NICSUMMARY = "NicSummary"
    HMRCPAYMENT = "HmrcPayment"
    DPSNOTICE = "DpsNotice"
    USER = "User"
    SETTINGS = "Settings"
    PAYRUN = "PayRun"
    LOAN = "Loan"
    DEPARTMENT = "Department"
    EMPLOYEROPENINGBALANCES = "EmployerOpeningBalances"
    EMPLOYERGROUPMEMBERSHIP = "EmployerGroupMembership"
    DEPARTMENTMEMBERSHIP = "DepartmentMembership"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)