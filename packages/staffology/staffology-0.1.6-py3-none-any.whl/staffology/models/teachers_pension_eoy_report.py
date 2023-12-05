from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.establishment import Establishment
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..models.teachers_pension_eoy_line_item import TeachersPensionEoyLineItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="TeachersPensionEoyReport")

@attr.s(auto_attribs=True)
class TeachersPensionEoyReport:
    """
    Attributes:
        pdf_file_name (Union[Unset, None, str]):
        establishment (Union[Unset, Establishment]):
        line_items (Union[Unset, None, List[TeachersPensionEoyLineItem]]):
        career_average_flexibilities (Union[Unset, float]):
        additional_pension_payments (Union[Unset, float]):
        additional_contributions (Union[Unset, float]):
        teachers_contributions (Union[Unset, float]):
        employers_contributions (Union[Unset, float]):
        total_contributions (Union[Unset, float]):
        efe_arrears (Union[Unset, float]):
        preston_contributions (Union[Unset, float]):
        tr_22_election_amounts (Union[Unset, float]):
        total_extra_contributions (Union[Unset, float]):
        overall_balance (Union[Unset, float]):
        employers_contribution_percentage (Union[Unset, float]):
        total_contributory_salary (Union[Unset, float]):
        total_teachers_contributions (Union[Unset, float]):
        total_employers_contributions (Union[Unset, float]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
        is_draft (Union[Unset, bool]):
    """

    pdf_file_name: Union[Unset, None, str] = UNSET
    establishment: Union[Unset, Establishment] = UNSET
    line_items: Union[Unset, None, List[TeachersPensionEoyLineItem]] = UNSET
    career_average_flexibilities: Union[Unset, float] = UNSET
    additional_pension_payments: Union[Unset, float] = UNSET
    additional_contributions: Union[Unset, float] = UNSET
    teachers_contributions: Union[Unset, float] = UNSET
    employers_contributions: Union[Unset, float] = UNSET
    total_contributions: Union[Unset, float] = UNSET
    efe_arrears: Union[Unset, float] = UNSET
    preston_contributions: Union[Unset, float] = UNSET
    tr_22_election_amounts: Union[Unset, float] = UNSET
    total_extra_contributions: Union[Unset, float] = UNSET
    overall_balance: Union[Unset, float] = UNSET
    employers_contribution_percentage: Union[Unset, float] = UNSET
    total_contributory_salary: Union[Unset, float] = UNSET
    total_teachers_contributions: Union[Unset, float] = UNSET
    total_employers_contributions: Union[Unset, float] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    is_draft: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pdf_file_name = self.pdf_file_name
        establishment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.establishment, Unset):
            establishment = self.establishment.to_dict()

        line_items: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.line_items, Unset):
            if self.line_items is None:
                line_items = None
            else:
                line_items = []
                for line_items_item_data in self.line_items:
                    line_items_item = line_items_item_data.to_dict()

                    line_items.append(line_items_item)




        career_average_flexibilities = self.career_average_flexibilities
        additional_pension_payments = self.additional_pension_payments
        additional_contributions = self.additional_contributions
        teachers_contributions = self.teachers_contributions
        employers_contributions = self.employers_contributions
        total_contributions = self.total_contributions
        efe_arrears = self.efe_arrears
        preston_contributions = self.preston_contributions
        tr_22_election_amounts = self.tr_22_election_amounts
        total_extra_contributions = self.total_extra_contributions
        overall_balance = self.overall_balance
        employers_contribution_percentage = self.employers_contribution_percentage
        total_contributory_salary = self.total_contributory_salary
        total_teachers_contributions = self.total_teachers_contributions
        total_employers_contributions = self.total_employers_contributions
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
        if pdf_file_name is not UNSET:
            field_dict["pdfFileName"] = pdf_file_name
        if establishment is not UNSET:
            field_dict["establishment"] = establishment
        if line_items is not UNSET:
            field_dict["lineItems"] = line_items
        if career_average_flexibilities is not UNSET:
            field_dict["careerAverageFlexibilities"] = career_average_flexibilities
        if additional_pension_payments is not UNSET:
            field_dict["additionalPensionPayments"] = additional_pension_payments
        if additional_contributions is not UNSET:
            field_dict["additionalContributions"] = additional_contributions
        if teachers_contributions is not UNSET:
            field_dict["teachersContributions"] = teachers_contributions
        if employers_contributions is not UNSET:
            field_dict["employersContributions"] = employers_contributions
        if total_contributions is not UNSET:
            field_dict["totalContributions"] = total_contributions
        if efe_arrears is not UNSET:
            field_dict["efeArrears"] = efe_arrears
        if preston_contributions is not UNSET:
            field_dict["prestonContributions"] = preston_contributions
        if tr_22_election_amounts is not UNSET:
            field_dict["tr22ElectionAmounts"] = tr_22_election_amounts
        if total_extra_contributions is not UNSET:
            field_dict["totalExtraContributions"] = total_extra_contributions
        if overall_balance is not UNSET:
            field_dict["overallBalance"] = overall_balance
        if employers_contribution_percentage is not UNSET:
            field_dict["employersContributionPercentage"] = employers_contribution_percentage
        if total_contributory_salary is not UNSET:
            field_dict["totalContributorySalary"] = total_contributory_salary
        if total_teachers_contributions is not UNSET:
            field_dict["totalTeachersContributions"] = total_teachers_contributions
        if total_employers_contributions is not UNSET:
            field_dict["totalEmployersContributions"] = total_employers_contributions
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
        pdf_file_name = d.pop("pdfFileName", UNSET)

        _establishment = d.pop("establishment", UNSET)
        establishment: Union[Unset, Establishment]
        if isinstance(_establishment,  Unset):
            establishment = UNSET
        else:
            establishment = Establishment.from_dict(_establishment)




        line_items = []
        _line_items = d.pop("lineItems", UNSET)
        for line_items_item_data in (_line_items or []):
            line_items_item = TeachersPensionEoyLineItem.from_dict(line_items_item_data)



            line_items.append(line_items_item)


        career_average_flexibilities = d.pop("careerAverageFlexibilities", UNSET)

        additional_pension_payments = d.pop("additionalPensionPayments", UNSET)

        additional_contributions = d.pop("additionalContributions", UNSET)

        teachers_contributions = d.pop("teachersContributions", UNSET)

        employers_contributions = d.pop("employersContributions", UNSET)

        total_contributions = d.pop("totalContributions", UNSET)

        efe_arrears = d.pop("efeArrears", UNSET)

        preston_contributions = d.pop("prestonContributions", UNSET)

        tr_22_election_amounts = d.pop("tr22ElectionAmounts", UNSET)

        total_extra_contributions = d.pop("totalExtraContributions", UNSET)

        overall_balance = d.pop("overallBalance", UNSET)

        employers_contribution_percentage = d.pop("employersContributionPercentage", UNSET)

        total_contributory_salary = d.pop("totalContributorySalary", UNSET)

        total_teachers_contributions = d.pop("totalTeachersContributions", UNSET)

        total_employers_contributions = d.pop("totalEmployersContributions", UNSET)

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

        teachers_pension_eoy_report = cls(
            pdf_file_name=pdf_file_name,
            establishment=establishment,
            line_items=line_items,
            career_average_flexibilities=career_average_flexibilities,
            additional_pension_payments=additional_pension_payments,
            additional_contributions=additional_contributions,
            teachers_contributions=teachers_contributions,
            employers_contributions=employers_contributions,
            total_contributions=total_contributions,
            efe_arrears=efe_arrears,
            preston_contributions=preston_contributions,
            tr_22_election_amounts=tr_22_election_amounts,
            total_extra_contributions=total_extra_contributions,
            overall_balance=overall_balance,
            employers_contribution_percentage=employers_contribution_percentage,
            total_contributory_salary=total_contributory_salary,
            total_teachers_contributions=total_teachers_contributions,
            total_employers_contributions=total_employers_contributions,
            report=report,
            tax_year=tax_year,
            is_draft=is_draft,
        )

        return teachers_pension_eoy_report

