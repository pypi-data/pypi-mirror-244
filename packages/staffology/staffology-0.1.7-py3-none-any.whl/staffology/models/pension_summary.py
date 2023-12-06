import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.pension_rule import PensionRule
from ..models.tiered_pension_rate import TieredPensionRate
from ..models.worker_group import WorkerGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionSummary")

@attr.s(auto_attribs=True)
class PensionSummary:
    """If a PayRunEntry contains pension contributions then it'll also include a PensionSummary model
giving further information about the Pension Scheme and the contributions made

    Attributes:
        pension_id (Union[Unset, str]): [readonly] The Id of the Pension.
        name (Union[Unset, None, str]): [readonly] The name of the PensionScheme to which contributions have been made.
        pension_scheme_id (Union[Unset, str]): [readonly] The Id of the PensionScheme.
        start_date (Union[Unset, datetime.date]): [readonly]
        worker_group_id (Union[Unset, str]): [readonly] The Id of the WorkerGroup.
        pension_rule (Union[Unset, PensionRule]):
        subtracted_basic_rate_tax (Union[Unset, bool]): [readonly] The SubtractedBasicRateTax applied from the
            PensionScheme SubtractBasicRateTax.
        papdis_pension_provider_id (Union[Unset, None, str]): [readonly] Papdis information from the PensionScheme
        papdis_employer_id (Union[Unset, None, str]): [readonly] Papdis information from the PensionScheme
        employee_pension_contribution_multiplier (Union[Unset, float]): [readonly] If the PensionScheme is set to
            SubtractBasicRateTax then this value  is used to reduce the contribution amount.
            Otherwise it is set as 1.
        additional_voluntary_contribution (Union[Unset, float]): [readonly] Any Additional Voluntary Contribution the
            Employee has chosen to make
            Otherwise it is set as 1.
        avc_is_percentage (Union[Unset, bool]): [readonly] Determines whether the Value of the Additional Voluntary
            Contribution is a fixed amount or a percentage,
        auto_enrolled (Union[Unset, bool]): [readonly] Any Additional Voluntary Contribution the Employee has chosen to
            make
            Otherwise it is set as 1.
        worker_group (Union[Unset, WorkerGroup]):
        forced_tier (Union[Unset, None, str]): [readonly] If the WorkerGroup ContributionLevelType is a Tiered Scheme
            then the name of the tier to force the employee on to may be specified.
            If none is specified then the Tier is determined by the earnings in the period
        tiers (Union[Unset, None, List[TieredPensionRate]]):
        assumed_pensionable_pay (Union[Unset, None, float]): [readonly] Assumed Pensionable Pay. If the employee is
            receiving any Statutory Leave that has an AssumedPensionablePay value set
            then it'll be shown here.
        pensionable_pay_codes (Union[Unset, None, List[str]]): [readonly] If the pension scheme is set to override the
            Pensionale PayCodes, then this is what they've been set to.
        is_half_contribution_member (Union[Unset, bool]): if an employee as a member of the 50/50 LGPS scheme, they can
            enable contribution to 50% of the normal contributions.
        pensionable_earnings (Union[Unset, float]): [readonly] The amount of the Gross that is subject to Pension
            Deductions.
            If the Pension Scheme uses Qualifying Earnings (upper and lower limits) then this value is before those are
            applied
            Applied only if an employee has more than one pension assigned to them
        pensionable_pay (Union[Unset, float]): [readonly] The amount of the Gross that pension calculations are based on
            after taking into account Upper and Lower Limits for the WorkerGroup.
            Applied only if an employee has more than one pension assigned to them
        non_tierable_pay (Union[Unset, float]): [readonly] The value of any pay that shouldn't count towards determining
            a pension tier.
        employee_pension_contribution (Union[Unset, float]): [readonly] The value of the Pension Contribution being made
            by this Employee, excluding any Additional Voluntary Contributions
        employee_pension_contribution_avc (Union[Unset, float]): [readonly] The value of the Pension Contribution being
            made by this Employee as an Additional Voluntary Contribution
        employer_pension_contribution (Union[Unset, float]): [readonly] The value of the Pension Contribution being made
            by the Employer for this Employee
        is_for_ended_pension (Union[Unset, bool]): [readonly] Determines whether the pension summary is related to a
            pension that has ended or not
        associated_employee_roles (Union[Unset, None, List[Item]]):
        pensionable_earnings_bfd (Union[Unset, float]): [readonly] The brought forward Year to Date amount of the Gross
            that is subject to Pension Deductions.
            Applied only if an employee has more than one pension assigned to them
        pensionable_pay_bfd (Union[Unset, float]): [readonly] The brought forward Year to Date amount of the Gross that
            pension calculations are based on after taking into account Upper and Lower Limits for the WorkerGroup.
            Applied only if an employee has more than one pension assigned to them
        employee_pension_contribution_bfd (Union[Unset, float]): [readonly] The brought forward Year to Date value of
            the Pension Contribution being made by this Employee, excluding any Additional Voluntary Contributions
        assumed_pensionable_pay_bfd (Union[Unset, None, float]): [readonly] The brought forward Year to Date value of
            Assumed Pensionable Pay. If the employee is receiving any Statutory Leave that has an AssumedPensionablePay
            value set
            then it'll be shown here.
        employer_pension_contribution_bfd (Union[Unset, float]): [readonly] The brought forward Year to Date value of
            the Pension Contribution being made by the Employer for this Employee
        employee_pension_contribution_avc_bfd (Union[Unset, float]): [readonly] The brought forward Year to Date value
            of the Pension Contribution being made by this Employee as an Additional Voluntary Contribution
    """

    pension_id: Union[Unset, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    pension_scheme_id: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    pension_rule: Union[Unset, PensionRule] = UNSET
    subtracted_basic_rate_tax: Union[Unset, bool] = UNSET
    papdis_pension_provider_id: Union[Unset, None, str] = UNSET
    papdis_employer_id: Union[Unset, None, str] = UNSET
    employee_pension_contribution_multiplier: Union[Unset, float] = UNSET
    additional_voluntary_contribution: Union[Unset, float] = UNSET
    avc_is_percentage: Union[Unset, bool] = UNSET
    auto_enrolled: Union[Unset, bool] = UNSET
    worker_group: Union[Unset, WorkerGroup] = UNSET
    forced_tier: Union[Unset, None, str] = UNSET
    tiers: Union[Unset, None, List[TieredPensionRate]] = UNSET
    assumed_pensionable_pay: Union[Unset, None, float] = UNSET
    pensionable_pay_codes: Union[Unset, None, List[str]] = UNSET
    is_half_contribution_member: Union[Unset, bool] = UNSET
    pensionable_earnings: Union[Unset, float] = UNSET
    pensionable_pay: Union[Unset, float] = UNSET
    non_tierable_pay: Union[Unset, float] = UNSET
    employee_pension_contribution: Union[Unset, float] = UNSET
    employee_pension_contribution_avc: Union[Unset, float] = UNSET
    employer_pension_contribution: Union[Unset, float] = UNSET
    is_for_ended_pension: Union[Unset, bool] = UNSET
    associated_employee_roles: Union[Unset, None, List[Item]] = UNSET
    pensionable_earnings_bfd: Union[Unset, float] = UNSET
    pensionable_pay_bfd: Union[Unset, float] = UNSET
    employee_pension_contribution_bfd: Union[Unset, float] = UNSET
    assumed_pensionable_pay_bfd: Union[Unset, None, float] = UNSET
    employer_pension_contribution_bfd: Union[Unset, float] = UNSET
    employee_pension_contribution_avc_bfd: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pension_id = self.pension_id
        name = self.name
        pension_scheme_id = self.pension_scheme_id
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        worker_group_id = self.worker_group_id
        pension_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pension_rule, Unset):
            pension_rule = self.pension_rule.value

        subtracted_basic_rate_tax = self.subtracted_basic_rate_tax
        papdis_pension_provider_id = self.papdis_pension_provider_id
        papdis_employer_id = self.papdis_employer_id
        employee_pension_contribution_multiplier = self.employee_pension_contribution_multiplier
        additional_voluntary_contribution = self.additional_voluntary_contribution
        avc_is_percentage = self.avc_is_percentage
        auto_enrolled = self.auto_enrolled
        worker_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.worker_group, Unset):
            worker_group = self.worker_group.to_dict()

        forced_tier = self.forced_tier
        tiers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tiers, Unset):
            if self.tiers is None:
                tiers = None
            else:
                tiers = []
                for tiers_item_data in self.tiers:
                    tiers_item = tiers_item_data.to_dict()

                    tiers.append(tiers_item)




        assumed_pensionable_pay = self.assumed_pensionable_pay
        pensionable_pay_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.pensionable_pay_codes, Unset):
            if self.pensionable_pay_codes is None:
                pensionable_pay_codes = None
            else:
                pensionable_pay_codes = self.pensionable_pay_codes




        is_half_contribution_member = self.is_half_contribution_member
        pensionable_earnings = self.pensionable_earnings
        pensionable_pay = self.pensionable_pay
        non_tierable_pay = self.non_tierable_pay
        employee_pension_contribution = self.employee_pension_contribution
        employee_pension_contribution_avc = self.employee_pension_contribution_avc
        employer_pension_contribution = self.employer_pension_contribution
        is_for_ended_pension = self.is_for_ended_pension
        associated_employee_roles: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associated_employee_roles, Unset):
            if self.associated_employee_roles is None:
                associated_employee_roles = None
            else:
                associated_employee_roles = []
                for associated_employee_roles_item_data in self.associated_employee_roles:
                    associated_employee_roles_item = associated_employee_roles_item_data.to_dict()

                    associated_employee_roles.append(associated_employee_roles_item)




        pensionable_earnings_bfd = self.pensionable_earnings_bfd
        pensionable_pay_bfd = self.pensionable_pay_bfd
        employee_pension_contribution_bfd = self.employee_pension_contribution_bfd
        assumed_pensionable_pay_bfd = self.assumed_pensionable_pay_bfd
        employer_pension_contribution_bfd = self.employer_pension_contribution_bfd
        employee_pension_contribution_avc_bfd = self.employee_pension_contribution_avc_bfd

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pension_id is not UNSET:
            field_dict["pensionId"] = pension_id
        if name is not UNSET:
            field_dict["name"] = name
        if pension_scheme_id is not UNSET:
            field_dict["pensionSchemeId"] = pension_scheme_id
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if pension_rule is not UNSET:
            field_dict["pensionRule"] = pension_rule
        if subtracted_basic_rate_tax is not UNSET:
            field_dict["subtractedBasicRateTax"] = subtracted_basic_rate_tax
        if papdis_pension_provider_id is not UNSET:
            field_dict["papdisPensionProviderId"] = papdis_pension_provider_id
        if papdis_employer_id is not UNSET:
            field_dict["papdisEmployerId"] = papdis_employer_id
        if employee_pension_contribution_multiplier is not UNSET:
            field_dict["employeePensionContributionMultiplier"] = employee_pension_contribution_multiplier
        if additional_voluntary_contribution is not UNSET:
            field_dict["additionalVoluntaryContribution"] = additional_voluntary_contribution
        if avc_is_percentage is not UNSET:
            field_dict["avcIsPercentage"] = avc_is_percentage
        if auto_enrolled is not UNSET:
            field_dict["autoEnrolled"] = auto_enrolled
        if worker_group is not UNSET:
            field_dict["workerGroup"] = worker_group
        if forced_tier is not UNSET:
            field_dict["forcedTier"] = forced_tier
        if tiers is not UNSET:
            field_dict["tiers"] = tiers
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if pensionable_pay_codes is not UNSET:
            field_dict["pensionablePayCodes"] = pensionable_pay_codes
        if is_half_contribution_member is not UNSET:
            field_dict["isHalfContributionMember"] = is_half_contribution_member
        if pensionable_earnings is not UNSET:
            field_dict["pensionableEarnings"] = pensionable_earnings
        if pensionable_pay is not UNSET:
            field_dict["pensionablePay"] = pensionable_pay
        if non_tierable_pay is not UNSET:
            field_dict["nonTierablePay"] = non_tierable_pay
        if employee_pension_contribution is not UNSET:
            field_dict["employeePensionContribution"] = employee_pension_contribution
        if employee_pension_contribution_avc is not UNSET:
            field_dict["employeePensionContributionAvc"] = employee_pension_contribution_avc
        if employer_pension_contribution is not UNSET:
            field_dict["employerPensionContribution"] = employer_pension_contribution
        if is_for_ended_pension is not UNSET:
            field_dict["isForEndedPension"] = is_for_ended_pension
        if associated_employee_roles is not UNSET:
            field_dict["associatedEmployeeRoles"] = associated_employee_roles
        if pensionable_earnings_bfd is not UNSET:
            field_dict["pensionableEarningsBfd"] = pensionable_earnings_bfd
        if pensionable_pay_bfd is not UNSET:
            field_dict["pensionablePayBfd"] = pensionable_pay_bfd
        if employee_pension_contribution_bfd is not UNSET:
            field_dict["employeePensionContributionBfd"] = employee_pension_contribution_bfd
        if assumed_pensionable_pay_bfd is not UNSET:
            field_dict["assumedPensionablePayBfd"] = assumed_pensionable_pay_bfd
        if employer_pension_contribution_bfd is not UNSET:
            field_dict["employerPensionContributionBfd"] = employer_pension_contribution_bfd
        if employee_pension_contribution_avc_bfd is not UNSET:
            field_dict["employeePensionContributionAvcBfd"] = employee_pension_contribution_avc_bfd

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pension_id = d.pop("pensionId", UNSET)

        name = d.pop("name", UNSET)

        pension_scheme_id = d.pop("pensionSchemeId", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date,  Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()




        worker_group_id = d.pop("workerGroupId", UNSET)

        _pension_rule = d.pop("pensionRule", UNSET)
        pension_rule: Union[Unset, PensionRule]
        if isinstance(_pension_rule,  Unset):
            pension_rule = UNSET
        else:
            pension_rule = PensionRule(_pension_rule)




        subtracted_basic_rate_tax = d.pop("subtractedBasicRateTax", UNSET)

        papdis_pension_provider_id = d.pop("papdisPensionProviderId", UNSET)

        papdis_employer_id = d.pop("papdisEmployerId", UNSET)

        employee_pension_contribution_multiplier = d.pop("employeePensionContributionMultiplier", UNSET)

        additional_voluntary_contribution = d.pop("additionalVoluntaryContribution", UNSET)

        avc_is_percentage = d.pop("avcIsPercentage", UNSET)

        auto_enrolled = d.pop("autoEnrolled", UNSET)

        _worker_group = d.pop("workerGroup", UNSET)
        worker_group: Union[Unset, WorkerGroup]
        if isinstance(_worker_group,  Unset):
            worker_group = UNSET
        else:
            worker_group = WorkerGroup.from_dict(_worker_group)




        forced_tier = d.pop("forcedTier", UNSET)

        tiers = []
        _tiers = d.pop("tiers", UNSET)
        for tiers_item_data in (_tiers or []):
            tiers_item = TieredPensionRate.from_dict(tiers_item_data)



            tiers.append(tiers_item)


        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        pensionable_pay_codes = cast(List[str], d.pop("pensionablePayCodes", UNSET))


        is_half_contribution_member = d.pop("isHalfContributionMember", UNSET)

        pensionable_earnings = d.pop("pensionableEarnings", UNSET)

        pensionable_pay = d.pop("pensionablePay", UNSET)

        non_tierable_pay = d.pop("nonTierablePay", UNSET)

        employee_pension_contribution = d.pop("employeePensionContribution", UNSET)

        employee_pension_contribution_avc = d.pop("employeePensionContributionAvc", UNSET)

        employer_pension_contribution = d.pop("employerPensionContribution", UNSET)

        is_for_ended_pension = d.pop("isForEndedPension", UNSET)

        associated_employee_roles = []
        _associated_employee_roles = d.pop("associatedEmployeeRoles", UNSET)
        for associated_employee_roles_item_data in (_associated_employee_roles or []):
            associated_employee_roles_item = Item.from_dict(associated_employee_roles_item_data)



            associated_employee_roles.append(associated_employee_roles_item)


        pensionable_earnings_bfd = d.pop("pensionableEarningsBfd", UNSET)

        pensionable_pay_bfd = d.pop("pensionablePayBfd", UNSET)

        employee_pension_contribution_bfd = d.pop("employeePensionContributionBfd", UNSET)

        assumed_pensionable_pay_bfd = d.pop("assumedPensionablePayBfd", UNSET)

        employer_pension_contribution_bfd = d.pop("employerPensionContributionBfd", UNSET)

        employee_pension_contribution_avc_bfd = d.pop("employeePensionContributionAvcBfd", UNSET)

        pension_summary = cls(
            pension_id=pension_id,
            name=name,
            pension_scheme_id=pension_scheme_id,
            start_date=start_date,
            worker_group_id=worker_group_id,
            pension_rule=pension_rule,
            subtracted_basic_rate_tax=subtracted_basic_rate_tax,
            papdis_pension_provider_id=papdis_pension_provider_id,
            papdis_employer_id=papdis_employer_id,
            employee_pension_contribution_multiplier=employee_pension_contribution_multiplier,
            additional_voluntary_contribution=additional_voluntary_contribution,
            avc_is_percentage=avc_is_percentage,
            auto_enrolled=auto_enrolled,
            worker_group=worker_group,
            forced_tier=forced_tier,
            tiers=tiers,
            assumed_pensionable_pay=assumed_pensionable_pay,
            pensionable_pay_codes=pensionable_pay_codes,
            is_half_contribution_member=is_half_contribution_member,
            pensionable_earnings=pensionable_earnings,
            pensionable_pay=pensionable_pay,
            non_tierable_pay=non_tierable_pay,
            employee_pension_contribution=employee_pension_contribution,
            employee_pension_contribution_avc=employee_pension_contribution_avc,
            employer_pension_contribution=employer_pension_contribution,
            is_for_ended_pension=is_for_ended_pension,
            associated_employee_roles=associated_employee_roles,
            pensionable_earnings_bfd=pensionable_earnings_bfd,
            pensionable_pay_bfd=pensionable_pay_bfd,
            employee_pension_contribution_bfd=employee_pension_contribution_bfd,
            assumed_pensionable_pay_bfd=assumed_pensionable_pay_bfd,
            employer_pension_contribution_bfd=employer_pension_contribution_bfd,
            employee_pension_contribution_avc_bfd=employee_pension_contribution_avc_bfd,
        )

        return pension_summary

