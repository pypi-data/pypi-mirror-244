from enum import Enum


class UserIndustry(str, Enum):
    NOTSPECIFIED = "NotSpecified"
    AGRICULTURE = "Agriculture"
    APPAREL = "Apparel"
    BANKING = "Banking"
    BIOTECHNOLOGY = "Biotechnology"
    CHEMICALS = "Chemicals"
    COMMUNICATION = "Communication"
    CONSTRUCTION = "Construction"
    CONSULTING = "Consulting"
    EDUCATION = "Education"
    ENGINEERING = "Engineering"
    ENTERTAINMENT = "Entertainment"
    ENVIRONMENTAL = "Environmental"
    FINANCE = "Finance"
    FOODANDBEVERAGE = "FoodAndBeverage"
    GOVERNMENT = "Government"
    HEALTHCARE = "Healthcare"
    HOSPITALITY = "Hospitality"
    INSURANCE = "Insurance"
    LEGAL = "Legal"
    MACHINERY = "Machinery"
    MANUFACTURING = "Manufacturing"
    MEDIA = "Media"
    NOTFORPROFIT = "NotForProfit"
    OTHER = "Other"
    RECREATION = "Recreation"
    RETAIL = "Retail"
    SHIPPING = "Shipping"
    TECHNOLOGY = "Technology"
    TELECOMMUNICATIONS = "Telecommunications"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
