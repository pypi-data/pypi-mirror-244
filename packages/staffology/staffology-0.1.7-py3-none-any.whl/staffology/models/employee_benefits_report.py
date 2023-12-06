from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeBenefitsReport")

@attr.s(auto_attribs=True)
class EmployeeBenefitsReport:
    """
    Attributes:
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
        is_draft (Union[Unset, bool]):
    """

    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    is_draft: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if is_draft is not UNSET:
            field_dict["isDraft"] = is_draft

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report,  Unset):
            report = UNSET
        else:
            report = Report(_report)




        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)




        is_draft = d.pop("isDraft", UNSET)

        employee_benefits_report = cls(
            report=report,
            tax_year=tax_year,
            is_draft=is_draft,
        )

        return employee_benefits_report

