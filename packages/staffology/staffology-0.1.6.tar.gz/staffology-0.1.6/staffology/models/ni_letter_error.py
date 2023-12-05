from enum import Enum


class NiLetterError(str, Enum):
    XNOTUSEDFORPENSIONERSPAYROLL = "XNotUsedForPensionersPayroll"
    BUSEDFORMALE = "BUsedForMale"
    CUSEDBEFORESTATEPENSIONAGE = "CUsedBeforeStatePensionAge"
    AUSEDFORUNDER21 = "AUsedForUnder21"
    AUSEDOVERSTATEPENSIONAGE = "AUsedOverStatePensionAge"
    HUSEDFOROVER24 = "HUsedForOver24"
    MUSEDFOROVER20 = "MUsedForOver20"
    ZUSEDFOROVER20 = "ZUsedForOver20"
    IUSEDFORMALE = "IUsedForMale"
    FUSEDFORNONFREEPORTWORKER = "FUsedForNonFreeportWorker"
    IUSEDFORNONFREEPORTWORKER = "IUsedForNonFreeportWorker"
    LUSEDFORNONFREEPORTWORKER = "LUsedForNonFreeportWorker"
    SUSEDFORNONFREEPORTWORKER = "SUsedForNonFreeportWorker"
    VUSEDFORNONVETERAN = "VUsedForNonVeteran"
    VUSEDFORVETERANSFIRSTEMPLOYMENTDATEOVERONEYEAROLD = "VUsedForVeteransFirstEmploymentDateOverOneYearOld"
    FUSEDFORFREEPORTWORKEROVERTHREEYEARSOLD = "FUsedForFreeportWorkerOverThreeYearsOld"
    IUSEDFORFREEPORTWORKEROVERTHREEYEARSOLD = "IUsedForFreeportWorkerOverThreeYearsOld"
    LUSEDFORFREEPORTWORKEROVERTHREEYEARSOLD = "LUsedForFreeportWorkerOverThreeYearsOld"
    SUSEDFORFREEPORTWORKEROVERTHREEYEARSOLD = "SUsedForFreeportWorkerOverThreeYearsOld"
    XNOTUSEDFORUNDER16 = "XNotUsedForUnder16"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)