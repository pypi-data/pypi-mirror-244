import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.ae_status import AeStatus
from ..models.item import Item
from ..models.pension_contribution_level_type import PensionContributionLevelType
from ..models.pension_end_reason import PensionEndReason
from ..models.pension_opening_balances import PensionOpeningBalances
from ..models.pension_scheme import PensionScheme
from ..models.teachers_pension_details import TeachersPensionDetails
from ..models.worker_group import WorkerGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="Pension")

@attr.s(auto_attribs=True)
class Pension:
    """
    Attributes:
        employee (Union[Unset, Item]):
        contribution_level_type (Union[Unset, PensionContributionLevelType]):
        end_date (Union[Unset, None, datetime.date]): The date the employee left the scheme
        end_reason (Union[Unset, PensionEndReason]):
        pension_opening_balances (Union[Unset, PensionOpeningBalances]):
        id (Union[Unset, str]): [readonly] The unique id of the object
        pension_scheme_id (Union[Unset, str]):
        pension_scheme (Union[Unset, PensionScheme]):
        worker_group_id (Union[Unset, str]):
        worker_group (Union[Unset, WorkerGroup]):
        start_date (Union[Unset, datetime.date]):
        member_reference_number (Union[Unset, None, str]):
        override_contributions (Union[Unset, bool]): If this is set to true then the Contributions levels set for the
            WorkerGroup will be replaced with the values provided here
        employee_contribution (Union[Unset, float]): The amount the employee contributes towards the pension. Could be a
            percentage or a fixed amount depending on EmployeeContributionIsPercentage.
            This is read-only if OverrideContributions is false
        employee_contribution_is_percentage (Union[Unset, bool]): Determines whether the Value of the
            EmployeeContribution is a fixed amount or a percentage,
        employer_contribution (Union[Unset, float]): The amount the employer contributes towards the pension. Could be a
            percentage or a fixed amount depending on EmployerContributionIsPercentage.
            This is read-only if OverrideContributions is false
        employer_contribution_is_percentage (Union[Unset, bool]): Determines whether the Value of the
            EmployerContribution is a fixed amount or a percentage,
        employer_contribution_top_up_percentage (Union[Unset, float]): Increase Employer Contribution by this percentage
            of the Employee Contribution
        is_ae_qualifying_scheme (Union[Unset, bool]): [readonly] Whether or not the associated PensionScheme is a
            Qualifying Scheme for AutoEnrolment
        is_teachers_pension (Union[Unset, bool]): [readonly] Whether or not the associated PensionScheme is a Teachers'
            Pension (determined by its CsvFormat)
        ae_status_at_joining (Union[Unset, AeStatus]):
        external_employee_id (Union[Unset, None, str]): [readonly]
        additional_voluntary_contribution (Union[Unset, float]): Any additional voluntary amount the employer
            contributes towards the pension. Could be a percentage or a fixed amount depending on AvcIsPercentage.
        avc_is_percentage (Union[Unset, bool]): Determines whether the Value of the Additional Voluntary Contribution is
            a fixed amount or a percentage,
        exit_via_provider (Union[Unset, bool]):
        teachers_pension_details (Union[Unset, TeachersPensionDetails]): Used to represent additional information needed
            for
            Teachers' Pensions
        forced_tier (Union[Unset, None, str]): If the WorkerGroup ContributionLevelType is a Tiered Scheme then you can
            specify the name of the tier to force the employee on to.
            If none is specified then the Tier is determined by the earnings in the period
        force_enrolment (Union[Unset, bool]): If the PensionScheme is connected to an ExternalDataProvider that supports
            enrolment then setting this to true will force this employee to be enrolled with the next submission.
        employer_contribution_includes_ni_saving (Union[Unset, bool]): Employer Contribution includes the Employers NI
            saving
        employer_contribution_ni_saving_percentage (Union[Unset, float]): Increase Employer Contribution by this
            percentage of the Employers NI saving
        fifty_fifty_scheme_member (Union[Unset, bool]): if an employee as a member of the 50/50 LGPS scheme, they can
            enable contribution to 50% of the normal contributions.
        associated_employee_roles (Union[Unset, None, List[Item]]): The list of employee roles associated with the
            pension membership
        auto_enrolled (Union[Unset, bool]): [readonly] Is True if the employee joined this Pension due to an
            AutoEnrolment action
    """

    employee: Union[Unset, Item] = UNSET
    contribution_level_type: Union[Unset, PensionContributionLevelType] = UNSET
    end_date: Union[Unset, None, datetime.date] = UNSET
    end_reason: Union[Unset, PensionEndReason] = UNSET
    pension_opening_balances: Union[Unset, PensionOpeningBalances] = UNSET
    id: Union[Unset, str] = UNSET
    pension_scheme_id: Union[Unset, str] = UNSET
    pension_scheme: Union[Unset, PensionScheme] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    worker_group: Union[Unset, WorkerGroup] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    member_reference_number: Union[Unset, None, str] = UNSET
    override_contributions: Union[Unset, bool] = UNSET
    employee_contribution: Union[Unset, float] = UNSET
    employee_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution: Union[Unset, float] = UNSET
    employer_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution_top_up_percentage: Union[Unset, float] = UNSET
    is_ae_qualifying_scheme: Union[Unset, bool] = UNSET
    is_teachers_pension: Union[Unset, bool] = UNSET
    ae_status_at_joining: Union[Unset, AeStatus] = UNSET
    external_employee_id: Union[Unset, None, str] = UNSET
    additional_voluntary_contribution: Union[Unset, float] = UNSET
    avc_is_percentage: Union[Unset, bool] = UNSET
    exit_via_provider: Union[Unset, bool] = UNSET
    teachers_pension_details: Union[Unset, TeachersPensionDetails] = UNSET
    forced_tier: Union[Unset, None, str] = UNSET
    force_enrolment: Union[Unset, bool] = UNSET
    employer_contribution_includes_ni_saving: Union[Unset, bool] = UNSET
    employer_contribution_ni_saving_percentage: Union[Unset, float] = UNSET
    fifty_fifty_scheme_member: Union[Unset, bool] = UNSET
    associated_employee_roles: Union[Unset, None, List[Item]] = UNSET
    auto_enrolled: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        contribution_level_type: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_level_type, Unset):
            contribution_level_type = self.contribution_level_type.value

        end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat() if self.end_date else None

        end_reason: Union[Unset, str] = UNSET
        if not isinstance(self.end_reason, Unset):
            end_reason = self.end_reason.value

        pension_opening_balances: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pension_opening_balances, Unset):
            pension_opening_balances = self.pension_opening_balances.to_dict()

        id = self.id
        pension_scheme_id = self.pension_scheme_id
        pension_scheme: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pension_scheme, Unset):
            pension_scheme = self.pension_scheme.to_dict()

        worker_group_id = self.worker_group_id
        worker_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.worker_group, Unset):
            worker_group = self.worker_group.to_dict()

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        member_reference_number = self.member_reference_number
        override_contributions = self.override_contributions
        employee_contribution = self.employee_contribution
        employee_contribution_is_percentage = self.employee_contribution_is_percentage
        employer_contribution = self.employer_contribution
        employer_contribution_is_percentage = self.employer_contribution_is_percentage
        employer_contribution_top_up_percentage = self.employer_contribution_top_up_percentage
        is_ae_qualifying_scheme = self.is_ae_qualifying_scheme
        is_teachers_pension = self.is_teachers_pension
        ae_status_at_joining: Union[Unset, str] = UNSET
        if not isinstance(self.ae_status_at_joining, Unset):
            ae_status_at_joining = self.ae_status_at_joining.value

        external_employee_id = self.external_employee_id
        additional_voluntary_contribution = self.additional_voluntary_contribution
        avc_is_percentage = self.avc_is_percentage
        exit_via_provider = self.exit_via_provider
        teachers_pension_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.teachers_pension_details, Unset):
            teachers_pension_details = self.teachers_pension_details.to_dict()

        forced_tier = self.forced_tier
        force_enrolment = self.force_enrolment
        employer_contribution_includes_ni_saving = self.employer_contribution_includes_ni_saving
        employer_contribution_ni_saving_percentage = self.employer_contribution_ni_saving_percentage
        fifty_fifty_scheme_member = self.fifty_fifty_scheme_member
        associated_employee_roles: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associated_employee_roles, Unset):
            if self.associated_employee_roles is None:
                associated_employee_roles = None
            else:
                associated_employee_roles = []
                for associated_employee_roles_item_data in self.associated_employee_roles:
                    associated_employee_roles_item = associated_employee_roles_item_data.to_dict()

                    associated_employee_roles.append(associated_employee_roles_item)




        auto_enrolled = self.auto_enrolled

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if employee is not UNSET:
            field_dict["employee"] = employee
        if contribution_level_type is not UNSET:
            field_dict["contributionLevelType"] = contribution_level_type
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if end_reason is not UNSET:
            field_dict["endReason"] = end_reason
        if pension_opening_balances is not UNSET:
            field_dict["pensionOpeningBalances"] = pension_opening_balances
        if id is not UNSET:
            field_dict["id"] = id
        if pension_scheme_id is not UNSET:
            field_dict["pensionSchemeId"] = pension_scheme_id
        if pension_scheme is not UNSET:
            field_dict["pensionScheme"] = pension_scheme
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if worker_group is not UNSET:
            field_dict["workerGroup"] = worker_group
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if member_reference_number is not UNSET:
            field_dict["memberReferenceNumber"] = member_reference_number
        if override_contributions is not UNSET:
            field_dict["overrideContributions"] = override_contributions
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
        if is_ae_qualifying_scheme is not UNSET:
            field_dict["isAeQualifyingScheme"] = is_ae_qualifying_scheme
        if is_teachers_pension is not UNSET:
            field_dict["isTeachersPension"] = is_teachers_pension
        if ae_status_at_joining is not UNSET:
            field_dict["aeStatusAtJoining"] = ae_status_at_joining
        if external_employee_id is not UNSET:
            field_dict["externalEmployeeId"] = external_employee_id
        if additional_voluntary_contribution is not UNSET:
            field_dict["additionalVoluntaryContribution"] = additional_voluntary_contribution
        if avc_is_percentage is not UNSET:
            field_dict["avcIsPercentage"] = avc_is_percentage
        if exit_via_provider is not UNSET:
            field_dict["exitViaProvider"] = exit_via_provider
        if teachers_pension_details is not UNSET:
            field_dict["teachersPensionDetails"] = teachers_pension_details
        if forced_tier is not UNSET:
            field_dict["forcedTier"] = forced_tier
        if force_enrolment is not UNSET:
            field_dict["forceEnrolment"] = force_enrolment
        if employer_contribution_includes_ni_saving is not UNSET:
            field_dict["employerContributionIncludesNiSaving"] = employer_contribution_includes_ni_saving
        if employer_contribution_ni_saving_percentage is not UNSET:
            field_dict["employerContributionNiSavingPercentage"] = employer_contribution_ni_saving_percentage
        if fifty_fifty_scheme_member is not UNSET:
            field_dict["fiftyFiftySchemeMember"] = fifty_fifty_scheme_member
        if associated_employee_roles is not UNSET:
            field_dict["associatedEmployeeRoles"] = associated_employee_roles
        if auto_enrolled is not UNSET:
            field_dict["autoEnrolled"] = auto_enrolled

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        _contribution_level_type = d.pop("contributionLevelType", UNSET)
        contribution_level_type: Union[Unset, PensionContributionLevelType]
        if isinstance(_contribution_level_type,  Unset):
            contribution_level_type = UNSET
        else:
            contribution_level_type = PensionContributionLevelType(_contribution_level_type)




        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, None, datetime.date]
        if _end_date is None:
            end_date = None
        elif isinstance(_end_date,  Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()




        _end_reason = d.pop("endReason", UNSET)
        end_reason: Union[Unset, PensionEndReason]
        if isinstance(_end_reason,  Unset):
            end_reason = UNSET
        else:
            end_reason = PensionEndReason(_end_reason)




        _pension_opening_balances = d.pop("pensionOpeningBalances", UNSET)
        pension_opening_balances: Union[Unset, PensionOpeningBalances]
        if isinstance(_pension_opening_balances,  Unset):
            pension_opening_balances = UNSET
        else:
            pension_opening_balances = PensionOpeningBalances.from_dict(_pension_opening_balances)




        id = d.pop("id", UNSET)

        pension_scheme_id = d.pop("pensionSchemeId", UNSET)

        _pension_scheme = d.pop("pensionScheme", UNSET)
        pension_scheme: Union[Unset, PensionScheme]
        if isinstance(_pension_scheme,  Unset):
            pension_scheme = UNSET
        else:
            pension_scheme = PensionScheme.from_dict(_pension_scheme)




        worker_group_id = d.pop("workerGroupId", UNSET)

        _worker_group = d.pop("workerGroup", UNSET)
        worker_group: Union[Unset, WorkerGroup]
        if isinstance(_worker_group,  Unset):
            worker_group = UNSET
        else:
            worker_group = WorkerGroup.from_dict(_worker_group)




        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date,  Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()




        member_reference_number = d.pop("memberReferenceNumber", UNSET)

        override_contributions = d.pop("overrideContributions", UNSET)

        employee_contribution = d.pop("employeeContribution", UNSET)

        employee_contribution_is_percentage = d.pop("employeeContributionIsPercentage", UNSET)

        employer_contribution = d.pop("employerContribution", UNSET)

        employer_contribution_is_percentage = d.pop("employerContributionIsPercentage", UNSET)

        employer_contribution_top_up_percentage = d.pop("employerContributionTopUpPercentage", UNSET)

        is_ae_qualifying_scheme = d.pop("isAeQualifyingScheme", UNSET)

        is_teachers_pension = d.pop("isTeachersPension", UNSET)

        _ae_status_at_joining = d.pop("aeStatusAtJoining", UNSET)
        ae_status_at_joining: Union[Unset, AeStatus]
        if isinstance(_ae_status_at_joining,  Unset):
            ae_status_at_joining = UNSET
        else:
            ae_status_at_joining = AeStatus(_ae_status_at_joining)




        external_employee_id = d.pop("externalEmployeeId", UNSET)

        additional_voluntary_contribution = d.pop("additionalVoluntaryContribution", UNSET)

        avc_is_percentage = d.pop("avcIsPercentage", UNSET)

        exit_via_provider = d.pop("exitViaProvider", UNSET)

        _teachers_pension_details = d.pop("teachersPensionDetails", UNSET)
        teachers_pension_details: Union[Unset, TeachersPensionDetails]
        if isinstance(_teachers_pension_details,  Unset):
            teachers_pension_details = UNSET
        else:
            teachers_pension_details = TeachersPensionDetails.from_dict(_teachers_pension_details)




        forced_tier = d.pop("forcedTier", UNSET)

        force_enrolment = d.pop("forceEnrolment", UNSET)

        employer_contribution_includes_ni_saving = d.pop("employerContributionIncludesNiSaving", UNSET)

        employer_contribution_ni_saving_percentage = d.pop("employerContributionNiSavingPercentage", UNSET)

        fifty_fifty_scheme_member = d.pop("fiftyFiftySchemeMember", UNSET)

        associated_employee_roles = []
        _associated_employee_roles = d.pop("associatedEmployeeRoles", UNSET)
        for associated_employee_roles_item_data in (_associated_employee_roles or []):
            associated_employee_roles_item = Item.from_dict(associated_employee_roles_item_data)



            associated_employee_roles.append(associated_employee_roles_item)


        auto_enrolled = d.pop("autoEnrolled", UNSET)

        pension = cls(
            employee=employee,
            contribution_level_type=contribution_level_type,
            end_date=end_date,
            end_reason=end_reason,
            pension_opening_balances=pension_opening_balances,
            id=id,
            pension_scheme_id=pension_scheme_id,
            pension_scheme=pension_scheme,
            worker_group_id=worker_group_id,
            worker_group=worker_group,
            start_date=start_date,
            member_reference_number=member_reference_number,
            override_contributions=override_contributions,
            employee_contribution=employee_contribution,
            employee_contribution_is_percentage=employee_contribution_is_percentage,
            employer_contribution=employer_contribution,
            employer_contribution_is_percentage=employer_contribution_is_percentage,
            employer_contribution_top_up_percentage=employer_contribution_top_up_percentage,
            is_ae_qualifying_scheme=is_ae_qualifying_scheme,
            is_teachers_pension=is_teachers_pension,
            ae_status_at_joining=ae_status_at_joining,
            external_employee_id=external_employee_id,
            additional_voluntary_contribution=additional_voluntary_contribution,
            avc_is_percentage=avc_is_percentage,
            exit_via_provider=exit_via_provider,
            teachers_pension_details=teachers_pension_details,
            forced_tier=forced_tier,
            force_enrolment=force_enrolment,
            employer_contribution_includes_ni_saving=employer_contribution_includes_ni_saving,
            employer_contribution_ni_saving_percentage=employer_contribution_ni_saving_percentage,
            fifty_fifty_scheme_member=fifty_fifty_scheme_member,
            associated_employee_roles=associated_employee_roles,
            auto_enrolled=auto_enrolled,
        )

        return pension

