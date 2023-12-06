from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.assumed_pensionable_pay import AssumedPensionablePay
from ..models.lgps_fund import LgpsFund
from ..models.pension_contribution_level_type import PensionContributionLevelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkerGroup")

@attr.s(auto_attribs=True)
class WorkerGroup:
    """
    Attributes:
        name (str):
        contribution_level_type (Union[Unset, PensionContributionLevelType]):
        employee_contribution (Union[Unset, float]):
        employee_contribution_is_percentage (Union[Unset, bool]):
        employer_contribution (Union[Unset, float]):
        employer_contribution_is_percentage (Union[Unset, bool]):
        employer_contribution_top_up_percentage (Union[Unset, float]): Increase Employer Contribution by this percentage
            of the Employee Contribution
        employer_contribution_includes_ni_saving (Union[Unset, bool]): Employer Contribution includes the Employers NI
            saving
        employer_contribution_ni_saving_percentage (Union[Unset, float]): Increase Employer Contribution by this
            percentage of the Employers NI saving
        is_avc (Union[Unset, bool]): Determines whether the workergroup uses additonal voluntary contributions.
            This property will automatically be set to true for the following Contribution Level Types: TpFasterAccrual,
            TpAdditionalPensionContributions, TpActuariallyAdjustedBenefits, TpFamilyBenefits, tpPastAddedYears,
            tpHigherSalaries, tpPreston, tpElectedFurtherEmployment, LgpsAdditionalPensionContributions,
            LgpsSharedAdditionalPensionContributions, LgpsAdditionalRegularContributions, LgpsAddedYearsContributions,
            LgpsSharedAdditionalPensionLumpSump, LgpsPartTimeBuyBack, PrudentialAVC.
        additional_voluntary_contribution (Union[Unset, None, float]): Any additional voluntary amount the employee
            contributes towards the pension. Could be a percentage or a fixed amount depending on AvcIsPercentage.
        avc_is_percentage (Union[Unset, None, bool]): Determines whether the Value of the Additional Voluntary
            Contribution is a fixed amount or a percentage,
        employer_contribution_ni_saving (Union[Unset, float]): Employers NI Saving
        custom_threshold (Union[Unset, bool]):
        lower_limit (Union[Unset, float]):
        upper_limit (Union[Unset, float]):
        papdis_group (Union[Unset, None, str]):
        papdis_sub_group (Union[Unset, None, str]):
        local_authority_number (Union[Unset, None, str]): Only applicable if ContributionLevelType is
            TeachersPensionEnglandAndWales
        school_employer_type (Union[Unset, None, str]): Only applicable if ContributionLevelType is
            TeachersPensionEnglandAndWales
        mat_identifier (Union[Unset, None, str]): Only applicable if ContributionLevelType is
            TeachersPensionEnglandAndWales
        mat_unique_number (Union[Unset, None, str]): Only applicable if ContributionLevelType is
            TeachersPensionEnglandAndWales
        employer_reference (Union[Unset, None, str]):
        lgps_fund (Union[Unset, LgpsFund]):
        worker_group_id (Union[Unset, str]): [readonly]
        assumed_pensionable_pay (Union[Unset, AssumedPensionablePay]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    contribution_level_type: Union[Unset, PensionContributionLevelType] = UNSET
    employee_contribution: Union[Unset, float] = UNSET
    employee_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution: Union[Unset, float] = UNSET
    employer_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution_top_up_percentage: Union[Unset, float] = UNSET
    employer_contribution_includes_ni_saving: Union[Unset, bool] = UNSET
    employer_contribution_ni_saving_percentage: Union[Unset, float] = UNSET
    is_avc: Union[Unset, bool] = UNSET
    additional_voluntary_contribution: Union[Unset, None, float] = UNSET
    avc_is_percentage: Union[Unset, None, bool] = UNSET
    employer_contribution_ni_saving: Union[Unset, float] = UNSET
    custom_threshold: Union[Unset, bool] = UNSET
    lower_limit: Union[Unset, float] = UNSET
    upper_limit: Union[Unset, float] = UNSET
    papdis_group: Union[Unset, None, str] = UNSET
    papdis_sub_group: Union[Unset, None, str] = UNSET
    local_authority_number: Union[Unset, None, str] = UNSET
    school_employer_type: Union[Unset, None, str] = UNSET
    mat_identifier: Union[Unset, None, str] = UNSET
    mat_unique_number: Union[Unset, None, str] = UNSET
    employer_reference: Union[Unset, None, str] = UNSET
    lgps_fund: Union[Unset, LgpsFund] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    assumed_pensionable_pay: Union[Unset, AssumedPensionablePay] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        contribution_level_type: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_level_type, Unset):
            contribution_level_type = self.contribution_level_type.value

        employee_contribution = self.employee_contribution
        employee_contribution_is_percentage = self.employee_contribution_is_percentage
        employer_contribution = self.employer_contribution
        employer_contribution_is_percentage = self.employer_contribution_is_percentage
        employer_contribution_top_up_percentage = self.employer_contribution_top_up_percentage
        employer_contribution_includes_ni_saving = self.employer_contribution_includes_ni_saving
        employer_contribution_ni_saving_percentage = self.employer_contribution_ni_saving_percentage
        is_avc = self.is_avc
        additional_voluntary_contribution = self.additional_voluntary_contribution
        avc_is_percentage = self.avc_is_percentage
        employer_contribution_ni_saving = self.employer_contribution_ni_saving
        custom_threshold = self.custom_threshold
        lower_limit = self.lower_limit
        upper_limit = self.upper_limit
        papdis_group = self.papdis_group
        papdis_sub_group = self.papdis_sub_group
        local_authority_number = self.local_authority_number
        school_employer_type = self.school_employer_type
        mat_identifier = self.mat_identifier
        mat_unique_number = self.mat_unique_number
        employer_reference = self.employer_reference
        lgps_fund: Union[Unset, str] = UNSET
        if not isinstance(self.lgps_fund, Unset):
            lgps_fund = self.lgps_fund.value

        worker_group_id = self.worker_group_id
        assumed_pensionable_pay: Union[Unset, str] = UNSET
        if not isinstance(self.assumed_pensionable_pay, Unset):
            assumed_pensionable_pay = self.assumed_pensionable_pay.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if contribution_level_type is not UNSET:
            field_dict["contributionLevelType"] = contribution_level_type
        if employee_contribution is not UNSET:
            field_dict["employeeContribution"] = employee_contribution
        if employee_contribution_is_percentage is not UNSET:
            field_dict["employeeContributionIsPercentage"] = employee_contribution_is_percentage
        if employer_contribution is not UNSET:
            field_dict["employerContribution"] = employer_contribution
        if employer_contribution_is_percentage is not UNSET:
            field_dict["employerContributionIsPercentage"] = employer_contribution_is_percentage
        if employer_contribution_top_up_percentage is not UNSET:
            field_dict["employerContributionTopUpPercentage"] = employer_contribution_top_up_percentage
        if employer_contribution_includes_ni_saving is not UNSET:
            field_dict["employerContributionIncludesNiSaving"] = employer_contribution_includes_ni_saving
        if employer_contribution_ni_saving_percentage is not UNSET:
            field_dict["employerContributionNiSavingPercentage"] = employer_contribution_ni_saving_percentage
        if is_avc is not UNSET:
            field_dict["isAvc"] = is_avc
        if additional_voluntary_contribution is not UNSET:
            field_dict["additionalVoluntaryContribution"] = additional_voluntary_contribution
        if avc_is_percentage is not UNSET:
            field_dict["avcIsPercentage"] = avc_is_percentage
        if employer_contribution_ni_saving is not UNSET:
            field_dict["employerContributionNiSaving"] = employer_contribution_ni_saving
        if custom_threshold is not UNSET:
            field_dict["customThreshold"] = custom_threshold
        if lower_limit is not UNSET:
            field_dict["lowerLimit"] = lower_limit
        if upper_limit is not UNSET:
            field_dict["upperLimit"] = upper_limit
        if papdis_group is not UNSET:
            field_dict["papdisGroup"] = papdis_group
        if papdis_sub_group is not UNSET:
            field_dict["papdisSubGroup"] = papdis_sub_group
        if local_authority_number is not UNSET:
            field_dict["localAuthorityNumber"] = local_authority_number
        if school_employer_type is not UNSET:
            field_dict["schoolEmployerType"] = school_employer_type
        if mat_identifier is not UNSET:
            field_dict["matIdentifier"] = mat_identifier
        if mat_unique_number is not UNSET:
            field_dict["matUniqueNumber"] = mat_unique_number
        if employer_reference is not UNSET:
            field_dict["employerReference"] = employer_reference
        if lgps_fund is not UNSET:
            field_dict["lgpsFund"] = lgps_fund
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _contribution_level_type = d.pop("contributionLevelType", UNSET)
        contribution_level_type: Union[Unset, PensionContributionLevelType]
        if isinstance(_contribution_level_type,  Unset):
            contribution_level_type = UNSET
        else:
            contribution_level_type = PensionContributionLevelType(_contribution_level_type)




        employee_contribution = d.pop("employeeContribution", UNSET)

        employee_contribution_is_percentage = d.pop("employeeContributionIsPercentage", UNSET)

        employer_contribution = d.pop("employerContribution", UNSET)

        employer_contribution_is_percentage = d.pop("employerContributionIsPercentage", UNSET)

        employer_contribution_top_up_percentage = d.pop("employerContributionTopUpPercentage", UNSET)

        employer_contribution_includes_ni_saving = d.pop("employerContributionIncludesNiSaving", UNSET)

        employer_contribution_ni_saving_percentage = d.pop("employerContributionNiSavingPercentage", UNSET)

        is_avc = d.pop("isAvc", UNSET)

        additional_voluntary_contribution = d.pop("additionalVoluntaryContribution", UNSET)

        avc_is_percentage = d.pop("avcIsPercentage", UNSET)

        employer_contribution_ni_saving = d.pop("employerContributionNiSaving", UNSET)

        custom_threshold = d.pop("customThreshold", UNSET)

        lower_limit = d.pop("lowerLimit", UNSET)

        upper_limit = d.pop("upperLimit", UNSET)

        papdis_group = d.pop("papdisGroup", UNSET)

        papdis_sub_group = d.pop("papdisSubGroup", UNSET)

        local_authority_number = d.pop("localAuthorityNumber", UNSET)

        school_employer_type = d.pop("schoolEmployerType", UNSET)

        mat_identifier = d.pop("matIdentifier", UNSET)

        mat_unique_number = d.pop("matUniqueNumber", UNSET)

        employer_reference = d.pop("employerReference", UNSET)

        _lgps_fund = d.pop("lgpsFund", UNSET)
        lgps_fund: Union[Unset, LgpsFund]
        if isinstance(_lgps_fund,  Unset):
            lgps_fund = UNSET
        else:
            lgps_fund = LgpsFund(_lgps_fund)




        worker_group_id = d.pop("workerGroupId", UNSET)

        _assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)
        assumed_pensionable_pay: Union[Unset, AssumedPensionablePay]
        if isinstance(_assumed_pensionable_pay,  Unset):
            assumed_pensionable_pay = UNSET
        else:
            assumed_pensionable_pay = AssumedPensionablePay(_assumed_pensionable_pay)




        id = d.pop("id", UNSET)

        worker_group = cls(
            name=name,
            contribution_level_type=contribution_level_type,
            employee_contribution=employee_contribution,
            employee_contribution_is_percentage=employee_contribution_is_percentage,
            employer_contribution=employer_contribution,
            employer_contribution_is_percentage=employer_contribution_is_percentage,
            employer_contribution_top_up_percentage=employer_contribution_top_up_percentage,
            employer_contribution_includes_ni_saving=employer_contribution_includes_ni_saving,
            employer_contribution_ni_saving_percentage=employer_contribution_ni_saving_percentage,
            is_avc=is_avc,
            additional_voluntary_contribution=additional_voluntary_contribution,
            avc_is_percentage=avc_is_percentage,
            employer_contribution_ni_saving=employer_contribution_ni_saving,
            custom_threshold=custom_threshold,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            papdis_group=papdis_group,
            papdis_sub_group=papdis_sub_group,
            local_authority_number=local_authority_number,
            school_employer_type=school_employer_type,
            mat_identifier=mat_identifier,
            mat_unique_number=mat_unique_number,
            employer_reference=employer_reference,
            lgps_fund=lgps_fund,
            worker_group_id=worker_group_id,
            assumed_pensionable_pay=assumed_pensionable_pay,
            id=id,
        )

        return worker_group

