import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.pension_contribution_level_type import PensionContributionLevelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeContribution")

@attr.s(auto_attribs=True)
class PapdisEmployeeContribution:
    """
    Attributes:
        employer_contributions_amount (Union[Unset, float]): [readonly]
        employer_contributions_percent (Union[Unset, float]): [readonly]
        employee_contributions_amount (Union[Unset, float]): [readonly]
        employee_contributions_percent (Union[Unset, float]): [readonly]
        additional_voluntary_contributions_amount (Union[Unset, float]): [readonly]
        additional_voluntary_contributions_percent (Union[Unset, float]): [readonly]
        salary_sacrifice_indicator (Union[Unset, bool]): [readonly]
        contribution_start_date (Union[Unset, datetime.date]): [readonly]
        employee_contribution_is_percentage (Union[Unset, bool]): [readonly]
        employer_contribution_is_percentage (Union[Unset, bool]): [readonly]
        unadjusted_employee_contributions_amount (Union[Unset, float]): [readonly]
        unadjusted_employer_contributions_amount (Union[Unset, float]): [readonly]
        unadjusted_additional_voluntary_contributions_amount (Union[Unset, float]): [readonly]
        employer_contribution_ni_savings (Union[Unset, float]): [readonly]
        contribution_level_type (Union[Unset, PensionContributionLevelType]):
        is_avc_only (Union[Unset, bool]): [readonly]
        employer_contribution_includes_ni_saving (Union[Unset, bool]): [readonly]
        unadjusted_additional_voluntary_contributions_percent (Union[Unset, float]): [readonly]
        is_half_contribution_member (Union[Unset, bool]): [readonly]
        assumed_pensionable_pay (Union[Unset, None, float]): [readonly]
        is_pension_refund (Union[Unset, bool]): [readonly]
    """

    employer_contributions_amount: Union[Unset, float] = UNSET
    employer_contributions_percent: Union[Unset, float] = UNSET
    employee_contributions_amount: Union[Unset, float] = UNSET
    employee_contributions_percent: Union[Unset, float] = UNSET
    additional_voluntary_contributions_amount: Union[Unset, float] = UNSET
    additional_voluntary_contributions_percent: Union[Unset, float] = UNSET
    salary_sacrifice_indicator: Union[Unset, bool] = UNSET
    contribution_start_date: Union[Unset, datetime.date] = UNSET
    employee_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution_is_percentage: Union[Unset, bool] = UNSET
    unadjusted_employee_contributions_amount: Union[Unset, float] = UNSET
    unadjusted_employer_contributions_amount: Union[Unset, float] = UNSET
    unadjusted_additional_voluntary_contributions_amount: Union[Unset, float] = UNSET
    employer_contribution_ni_savings: Union[Unset, float] = UNSET
    contribution_level_type: Union[Unset, PensionContributionLevelType] = UNSET
    is_avc_only: Union[Unset, bool] = UNSET
    employer_contribution_includes_ni_saving: Union[Unset, bool] = UNSET
    unadjusted_additional_voluntary_contributions_percent: Union[Unset, float] = UNSET
    is_half_contribution_member: Union[Unset, bool] = UNSET
    assumed_pensionable_pay: Union[Unset, None, float] = UNSET
    is_pension_refund: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        employer_contributions_amount = self.employer_contributions_amount
        employer_contributions_percent = self.employer_contributions_percent
        employee_contributions_amount = self.employee_contributions_amount
        employee_contributions_percent = self.employee_contributions_percent
        additional_voluntary_contributions_amount = self.additional_voluntary_contributions_amount
        additional_voluntary_contributions_percent = self.additional_voluntary_contributions_percent
        salary_sacrifice_indicator = self.salary_sacrifice_indicator
        contribution_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_start_date, Unset):
            contribution_start_date = self.contribution_start_date.isoformat()

        employee_contribution_is_percentage = self.employee_contribution_is_percentage
        employer_contribution_is_percentage = self.employer_contribution_is_percentage
        unadjusted_employee_contributions_amount = self.unadjusted_employee_contributions_amount
        unadjusted_employer_contributions_amount = self.unadjusted_employer_contributions_amount
        unadjusted_additional_voluntary_contributions_amount = self.unadjusted_additional_voluntary_contributions_amount
        employer_contribution_ni_savings = self.employer_contribution_ni_savings
        contribution_level_type: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_level_type, Unset):
            contribution_level_type = self.contribution_level_type.value

        is_avc_only = self.is_avc_only
        employer_contribution_includes_ni_saving = self.employer_contribution_includes_ni_saving
        unadjusted_additional_voluntary_contributions_percent = self.unadjusted_additional_voluntary_contributions_percent
        is_half_contribution_member = self.is_half_contribution_member
        assumed_pensionable_pay = self.assumed_pensionable_pay
        is_pension_refund = self.is_pension_refund

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if employer_contributions_amount is not UNSET:
            field_dict["employerContributionsAmount"] = employer_contributions_amount
        if employer_contributions_percent is not UNSET:
            field_dict["employerContributionsPercent"] = employer_contributions_percent
        if employee_contributions_amount is not UNSET:
            field_dict["employeeContributionsAmount"] = employee_contributions_amount
        if employee_contributions_percent is not UNSET:
            field_dict["employeeContributionsPercent"] = employee_contributions_percent
        if additional_voluntary_contributions_amount is not UNSET:
            field_dict["additionalVoluntaryContributionsAmount"] = additional_voluntary_contributions_amount
        if additional_voluntary_contributions_percent is not UNSET:
            field_dict["additionalVoluntaryContributionsPercent"] = additional_voluntary_contributions_percent
        if salary_sacrifice_indicator is not UNSET:
            field_dict["salarySacrificeIndicator"] = salary_sacrifice_indicator
        if contribution_start_date is not UNSET:
            field_dict["contributionStartDate"] = contribution_start_date
        if employee_contribution_is_percentage is not UNSET:
            field_dict["employeeContributionIsPercentage"] = employee_contribution_is_percentage
        if employer_contribution_is_percentage is not UNSET:
            field_dict["employerContributionIsPercentage"] = employer_contribution_is_percentage
        if unadjusted_employee_contributions_amount is not UNSET:
            field_dict["unadjustedEmployeeContributionsAmount"] = unadjusted_employee_contributions_amount
        if unadjusted_employer_contributions_amount is not UNSET:
            field_dict["unadjustedEmployerContributionsAmount"] = unadjusted_employer_contributions_amount
        if unadjusted_additional_voluntary_contributions_amount is not UNSET:
            field_dict["unadjustedAdditionalVoluntaryContributionsAmount"] = unadjusted_additional_voluntary_contributions_amount
        if employer_contribution_ni_savings is not UNSET:
            field_dict["employerContributionNiSavings"] = employer_contribution_ni_savings
        if contribution_level_type is not UNSET:
            field_dict["contributionLevelType"] = contribution_level_type
        if is_avc_only is not UNSET:
            field_dict["isAvcOnly"] = is_avc_only
        if employer_contribution_includes_ni_saving is not UNSET:
            field_dict["employerContributionIncludesNiSaving"] = employer_contribution_includes_ni_saving
        if unadjusted_additional_voluntary_contributions_percent is not UNSET:
            field_dict["unadjustedAdditionalVoluntaryContributionsPercent"] = unadjusted_additional_voluntary_contributions_percent
        if is_half_contribution_member is not UNSET:
            field_dict["isHalfContributionMember"] = is_half_contribution_member
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if is_pension_refund is not UNSET:
            field_dict["isPensionRefund"] = is_pension_refund

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_contributions_amount = d.pop("employerContributionsAmount", UNSET)

        employer_contributions_percent = d.pop("employerContributionsPercent", UNSET)

        employee_contributions_amount = d.pop("employeeContributionsAmount", UNSET)

        employee_contributions_percent = d.pop("employeeContributionsPercent", UNSET)

        additional_voluntary_contributions_amount = d.pop("additionalVoluntaryContributionsAmount", UNSET)

        additional_voluntary_contributions_percent = d.pop("additionalVoluntaryContributionsPercent", UNSET)

        salary_sacrifice_indicator = d.pop("salarySacrificeIndicator", UNSET)

        _contribution_start_date = d.pop("contributionStartDate", UNSET)
        contribution_start_date: Union[Unset, datetime.date]
        if isinstance(_contribution_start_date,  Unset):
            contribution_start_date = UNSET
        else:
            contribution_start_date = isoparse(_contribution_start_date).date()




        employee_contribution_is_percentage = d.pop("employeeContributionIsPercentage", UNSET)

        employer_contribution_is_percentage = d.pop("employerContributionIsPercentage", UNSET)

        unadjusted_employee_contributions_amount = d.pop("unadjustedEmployeeContributionsAmount", UNSET)

        unadjusted_employer_contributions_amount = d.pop("unadjustedEmployerContributionsAmount", UNSET)

        unadjusted_additional_voluntary_contributions_amount = d.pop("unadjustedAdditionalVoluntaryContributionsAmount", UNSET)

        employer_contribution_ni_savings = d.pop("employerContributionNiSavings", UNSET)

        _contribution_level_type = d.pop("contributionLevelType", UNSET)
        contribution_level_type: Union[Unset, PensionContributionLevelType]
        if isinstance(_contribution_level_type,  Unset):
            contribution_level_type = UNSET
        else:
            contribution_level_type = PensionContributionLevelType(_contribution_level_type)




        is_avc_only = d.pop("isAvcOnly", UNSET)

        employer_contribution_includes_ni_saving = d.pop("employerContributionIncludesNiSaving", UNSET)

        unadjusted_additional_voluntary_contributions_percent = d.pop("unadjustedAdditionalVoluntaryContributionsPercent", UNSET)

        is_half_contribution_member = d.pop("isHalfContributionMember", UNSET)

        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        is_pension_refund = d.pop("isPensionRefund", UNSET)

        papdis_employee_contribution = cls(
            employer_contributions_amount=employer_contributions_amount,
            employer_contributions_percent=employer_contributions_percent,
            employee_contributions_amount=employee_contributions_amount,
            employee_contributions_percent=employee_contributions_percent,
            additional_voluntary_contributions_amount=additional_voluntary_contributions_amount,
            additional_voluntary_contributions_percent=additional_voluntary_contributions_percent,
            salary_sacrifice_indicator=salary_sacrifice_indicator,
            contribution_start_date=contribution_start_date,
            employee_contribution_is_percentage=employee_contribution_is_percentage,
            employer_contribution_is_percentage=employer_contribution_is_percentage,
            unadjusted_employee_contributions_amount=unadjusted_employee_contributions_amount,
            unadjusted_employer_contributions_amount=unadjusted_employer_contributions_amount,
            unadjusted_additional_voluntary_contributions_amount=unadjusted_additional_voluntary_contributions_amount,
            employer_contribution_ni_savings=employer_contribution_ni_savings,
            contribution_level_type=contribution_level_type,
            is_avc_only=is_avc_only,
            employer_contribution_includes_ni_saving=employer_contribution_includes_ni_saving,
            unadjusted_additional_voluntary_contributions_percent=unadjusted_additional_voluntary_contributions_percent,
            is_half_contribution_member=is_half_contribution_member,
            assumed_pensionable_pay=assumed_pensionable_pay,
            is_pension_refund=is_pension_refund,
        )

        return papdis_employee_contribution

