from enum import Enum


class BankPaymentInstructionsCsvFormat(str, Enum):
    STANDARDCSV = "StandardCsv"
    TELLEROO = "Telleroo"
    BARCLAYSBACS = "BarclaysBacs"
    SANTANDERBACS = "SantanderBacs"
    SIF = "Sif"
    REVOLUT = "Revolut"
    STANDARD18FASTERPAYMENTS = "Standard18FasterPayments"
    STANDARD18BACS = "Standard18Bacs"
    BANKLINE = "Bankline"
    BANKLINEBULK = "BanklineBulk"
    STANDARDCSVBACS = "StandardCsvBacs"
    LLOYDSMULTIPLESTANDARDCSVBACS = "LloydsMultipleStandardCsvBacs"
    LLOYDSV11CSVBACS = "LloydsV11CsvBacs"
    COOPBULKCSVBACS = "CoOpBulkCsvBacs"
    COOPFASTERPAYMENTSCSV = "CoOpFasterPaymentsCsv"
    BANKOFAMERICABACS = "BankOfAmericaBacs"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        #  Staffology API sometimes sends the index value inside an enum instead of the value of the enum itself
        value_from_index = list(dict(cls.__members__).values())[int(value)]
        return cls(value_from_index)
