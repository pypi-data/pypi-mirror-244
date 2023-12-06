from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_periods import PayPeriods
from ..models.report_format import ReportFormat
from ..models.report_sort_by import ReportSortBy
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractGrossToNetReportRequest")

@attr.s(auto_attribs=True)
class ContractGrossToNetReportRequest:
    """
    Attributes:
        pay_period (Union[Unset, PayPeriods]):
        tax_year (Union[Unset, TaxYear]):
        from_period (Union[Unset, int]): The start Tax Month of report data.
        to_period (Union[Unset, int]): The end Tax Month of report data.
        report_format (Union[Unset, ReportFormat]):
        sort_by (Union[Unset, ReportSortBy]):
        sort_descending (Union[Unset, bool]): Defines whether to sort the data in descending order. Defaults to false.
        ordinal (Union[Unset, int]): Indicates whether this uses first, second, third (etc.) PaySchedule for this
            PayPeriod.
        for_cis (Union[Unset, bool]): If true then CIS Subcontractors are reported on.
    """

    pay_period: Union[Unset, PayPeriods] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    from_period: Union[Unset, int] = UNSET
    to_period: Union[Unset, int] = UNSET
    report_format: Union[Unset, ReportFormat] = UNSET
    sort_by: Union[Unset, ReportSortBy] = UNSET
    sort_descending: Union[Unset, bool] = UNSET
    ordinal: Union[Unset, int] = UNSET
    for_cis: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        from_period = self.from_period
        to_period = self.to_period
        report_format: Union[Unset, str] = UNSET
        if not isinstance(self.report_format, Unset):
            report_format = self.report_format.value

        sort_by: Union[Unset, str] = UNSET
        if not isinstance(self.sort_by, Unset):
            sort_by = self.sort_by.value

        sort_descending = self.sort_descending
        ordinal = self.ordinal
        for_cis = self.for_cis

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if from_period is not UNSET:
            field_dict["fromPeriod"] = from_period
        if to_period is not UNSET:
            field_dict["toPeriod"] = to_period
        if report_format is not UNSET:
            field_dict["reportFormat"] = report_format
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by
        if sort_descending is not UNSET:
            field_dict["sortDescending"] = sort_descending
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if for_cis is not UNSET:
            field_dict["forCis"] = for_cis

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period,  Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)




        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)




        from_period = d.pop("fromPeriod", UNSET)

        to_period = d.pop("toPeriod", UNSET)

        _report_format = d.pop("reportFormat", UNSET)
        report_format: Union[Unset, ReportFormat]
        if isinstance(_report_format,  Unset):
            report_format = UNSET
        else:
            report_format = ReportFormat(_report_format)




        _sort_by = d.pop("sortBy", UNSET)
        sort_by: Union[Unset, ReportSortBy]
        if isinstance(_sort_by,  Unset):
            sort_by = UNSET
        else:
            sort_by = ReportSortBy(_sort_by)




        sort_descending = d.pop("sortDescending", UNSET)

        ordinal = d.pop("ordinal", UNSET)

        for_cis = d.pop("forCis", UNSET)

        contract_gross_to_net_report_request = cls(
            pay_period=pay_period,
            tax_year=tax_year,
            from_period=from_period,
            to_period=to_period,
            report_format=report_format,
            sort_by=sort_by,
            sort_descending=sort_descending,
            ordinal=ordinal,
            for_cis=for_cis,
        )

        return contract_gross_to_net_report_request

