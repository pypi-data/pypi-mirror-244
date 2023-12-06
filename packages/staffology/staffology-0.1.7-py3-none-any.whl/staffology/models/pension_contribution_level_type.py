from enum import Enum


class PensionContributionLevelType(str, Enum):
    USERDEFINED = "UserDefined"
    STATUTORYMINIMUM = "StatutoryMinimum"
    NHS2015 = "Nhs2015"
    TEACHERSPENSIONENGLANDANDWALES = "TeachersPensionEnglandAndWales"
    LGPSENGLANDANDWALES = "LgpsEnglandAndWales"
    TPFASTERACCRUAL = "TpFasterAccrual"
    TPADDITIONALPENSIONCONTRIBUTIONS = "TpAdditionalPensionContributions"
    TPACTUARIALLYADJUSTEDBENEFITS = "TpActuariallyAdjustedBenefits"
    TPFAMILYBENEFITS = "TpFamilyBenefits"
    TPPASTADDEDYEARS = "tpPastAddedYears"
    TPHIGHERSALARIES = "tpHigherSalaries"
    TPPRESTON = "tpPreston"
    LGPSADDITIONALPENSIONCONTRIBUTIONS = "LgpsAdditionalPensionContributions"
    LGPSSHAREDADDITIONALPENSIONCONTRIBUTIONS = "LgpsSharedAdditionalPensionContributions"
    LGPSADDITIONALREGULARCONTRIBUTIONS = "LgpsAdditionalRegularContributions"
    LGPSADDEDYEARSCONTRIBUTIONS = "LgpsAddedYearsContributions"
    LGPSSHAREDADDITIONALPENSIONLUMPSUMP = "LgpsSharedAdditionalPensionLumpSump"
    LGPSPARTTIMEBUYBACK = "LgpsPartTimeBuyBack"
    PRUDENTIALAVC = "PrudentialAVC"
    TPELECTEDFURTHEREMPLOYMENT = "tpElectedFurtherEmployment"
    APTISCASHISA = "AptisCashIsa"
    APTISSTOCKSSHARESISA = "AptisStocksSharesIsa"
    APTISINVESTMENTACCOUNT = "AptisInvestmentAccount"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
