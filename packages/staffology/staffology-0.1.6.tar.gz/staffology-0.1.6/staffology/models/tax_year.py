from enum import Enum


class TaxYear(str, Enum):
    YEAR2017 = "Year2017"
    YEAR2018 = "Year2018"
    YEAR2019 = "Year2019"
    YEAR2020 = "Year2020"
    YEAR2021 = "Year2021"
    YEAR2022 = "Year2022"
    YEAR2023 = "Year2023"
    YEAR2024 = "Year2024"
    YEAR2025 = "Year2025"
    YEAR2026 = "Year2026"
    YEAR2027 = "Year2027"
    YEAR2028 = "Year2028"
    YEAR2029 = "Year2029"
    YEAR2030 = "Year2030"
    YEAR2031 = "Year2031"
    YEAR2032 = "Year2032"
    YEAR2033 = "Year2033"
    YEAR2034 = "Year2034"
    YEAR2035 = "Year2035"
    YEAR2036 = "Year2036"
    YEAR2037 = "Year2037"
    YEAR2038 = "Year2038"
    YEAR2039 = "Year2039"
    YEAR2040 = "Year2040"
    YEAR2041 = "Year2041"
    YEAR2042 = "Year2042"
    YEAR2043 = "Year2043"
    YEAR2044 = "Year2044"
    YEAR2045 = "Year2045"
    YEAR2046 = "Year2046"
    YEAR2047 = "Year2047"
    YEAR2048 = "Year2048"
    YEAR2049 = "Year2049"
    YEAR2050 = "Year2050"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)