from enum import Enum


class PayRunEntryWarningType(str, Enum):
    MISSINGBANKDETAILS = "MissingBankDetails"
    MISSINGADDRESSLINES = "MissingAddressLines"
    ADDRESSINVALID = "AddressInvalid"
    NINOINVALID = "NinoInvalid"
    BELOWNATIONALMINIMUMWAGE = "BelowNationalMinimumWage"
    HIGHGROSSPAY = "HighGrossPay"
    HIGHNETPAY = "HighNetPay"
    INRECEIPTOFTAXREFUND = "InReceiptOfTaxRefund"
    NETTOGROSSDISCREPANCYABOVETHRESHOLD = "NetToGrossDiscrepancyAboveThreshold"
    STATUTORYMATERNITY = "StatutoryMaternity"
    TEACHERSPENSIONNOTAUTOCALCULATED = "TeachersPensionNotAutoCalculated"
    JOINTTEACHERSPENSIONSNOTAUTOCALCULATED = "JointTeachersPensionsNotAutoCalculated"
    MISSINGNINUMBER = "MissingNiNumber"

    def __str__(self) -> str:
        return str(self.value)
