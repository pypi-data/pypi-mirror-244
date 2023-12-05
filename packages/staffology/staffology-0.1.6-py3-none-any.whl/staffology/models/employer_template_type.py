from enum import Enum


class EmployerTemplateType(str, Enum):
    PAYSLIPEMAIL = "PayslipEmail"
    AUTOENROLMENT_ENROLLED = "AutoEnrolment_Enrolled"
    AUTOENROLMENT_ENROLLED_NETPAY = "AutoEnrolment_Enrolled_NetPay"
    AUTOENROLMENT_NOTENROLLED = "AutoEnrolment_NotEnrolled"
    AUTOENROLMENT_INSERT = "AutoEnrolment_Insert"
    CISSTATEMENTEMAIL = "CisStatementEmail"
    PAYRUNSUMMARY = "PayrunSummary"
    PAYSLIPSUNEMAILED = "PayslipsUnemailed"
    PAYRUNAUTOEMAIL = "PayrunAutoEmail"
    P60EMAIL = "P60Email"
    ANNUALCISSTATEMENTEMAIL = "AnnualCisStatementEmail"
    P45EMAIL = "P45Email"
    AUTOENROLMENT_POSTPONED = "AutoEnrolment_Postponed"
    AUTOENROLMENT_REENROLLED = "AutoEnrolment_ReEnrolled"
    AUTOENROLMENT_ENROLLED_SALARYSACRIFICE = "AutoEnrolment_Enrolled_SalarySacrifice"
    AUTOENROLMENT_REENROLLED_SALARYSACRIFICE = "AutoEnrolment_ReEnrolled_SalarySacrifice"
    P11DEMAIL = "P11DEmail"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
