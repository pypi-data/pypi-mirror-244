from enum import Enum


class PensionCsvFormat(str, Enum):
    PAPDIS = "Papdis"
    NEST = "Nest"
    NOWPENSIONS = "NowPensions"
    TEACHERSPENSIONMDC = "TeachersPensionMdc"
    TEACHERSPENSIONMCR = "TeachersPensionMcr"
    SCOTTISHWIDOWSASSISTME = "ScottishWidowsAssistMe"
    AVIVA = "Aviva"
    AVIVAENROLMENT = "AvivaEnrolment"
    SCOTTISHWIDOWSWORKPLACE = "ScottishWidowsWorkplace"
    AEGON = "Aegon"
    SCOTTISHWIDOWSWORKPLACEENROLMENT = "ScottishWidowsWorkplaceEnrolment"
    AEGONENROLMENT = "AegonEnrolment"
    STANDARDLIFEWORKPLACEHUB = "StandardLifeWorkplaceHub"
    PEOPLESPENSION = "PeoplesPension"
    STANDARDLIFEWORKPLACEHUBENROLMENT = "StandardLifeWorkplaceHubEnrolment"
    PRUDENTIALAVC = "PrudentialAvc"
    LGPSCIVICAUPM = "LgpsCivicaUpm"
    LGPSICONNECT = "LgpsIConnect"
    STANDARDLIFEGPZ = "StandardLifeGpz"
    STANDARDLIFEGPZENROLMENT = "StandardLifeGpzEnrolment"
    APTIS = "Aptis"
    APTISENROLMENT = "AptisEnrolment"
    NESTENROLMENT = "NestEnrolment"

    def __str__(self) -> str:
        return str(self.value)
