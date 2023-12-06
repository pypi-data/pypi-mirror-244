from enum import Enum


class PdfPaperSize(str, Enum):
    LETTER = "Letter"
    LETTERSMALL = "LetterSmall"
    A4 = "A4"
    A4SMALL = "A4Small"
    A5 = "A5"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)