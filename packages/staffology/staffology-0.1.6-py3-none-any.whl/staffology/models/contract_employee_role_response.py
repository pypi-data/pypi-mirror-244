import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.contract_pay_options_base_response import ContractPayOptionsBaseResponse
from ..models.contract_working_pattern_response import ContractWorkingPatternResponse
from ..models.role_basis import RoleBasis
from ..models.role_type import RoleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractEmployeeRoleResponse")

@attr.s(auto_attribs=True)
class ContractEmployeeRoleResponse:
    """
    Attributes:
        id (Union[Unset, str]):
        job_title (Union[Unset, None, str]): Job Title of the Role
        is_primary (Union[Unset, bool]): Set to True if this is Primary role of the Employee
        reference (Union[Unset, None, str]):
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, None, datetime.date]):
        basis (Union[Unset, RoleBasis]):
        type (Union[Unset, RoleType]):
        display_name (Union[Unset, None, str]):
        pay_options (Union[Unset, ContractPayOptionsBaseResponse]):
        working_pattern (Union[Unset, ContractWorkingPatternResponse]):
        occupational_maternity_policy_unique_id (Union[Unset, None, str]):
        occupational_sickness_policy_unique_id (Union[Unset, None, str]):
    """

    id: Union[Unset, str] = UNSET
    job_title: Union[Unset, None, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    reference: Union[Unset, None, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, None, datetime.date] = UNSET
    basis: Union[Unset, RoleBasis] = UNSET
    type: Union[Unset, RoleType] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    pay_options: Union[Unset, ContractPayOptionsBaseResponse] = UNSET
    working_pattern: Union[Unset, ContractWorkingPatternResponse] = UNSET
    occupational_maternity_policy_unique_id: Union[Unset, None, str] = UNSET
    occupational_sickness_policy_unique_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        job_title = self.job_title
        is_primary = self.is_primary
        reference = self.reference
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat() if self.end_date else None

        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        display_name = self.display_name
        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        working_pattern: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.working_pattern, Unset):
            working_pattern = self.working_pattern.to_dict()

        occupational_maternity_policy_unique_id = self.occupational_maternity_policy_unique_id
        occupational_sickness_policy_unique_id = self.occupational_sickness_policy_unique_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary
        if reference is not UNSET:
            field_dict["reference"] = reference
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if basis is not UNSET:
            field_dict["basis"] = basis
        if type is not UNSET:
            field_dict["type"] = type
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options
        if working_pattern is not UNSET:
            field_dict["workingPattern"] = working_pattern
        if occupational_maternity_policy_unique_id is not UNSET:
            field_dict["occupationalMaternityPolicyUniqueId"] = occupational_maternity_policy_unique_id
        if occupational_sickness_policy_unique_id is not UNSET:
            field_dict["occupationalSicknessPolicyUniqueId"] = occupational_sickness_policy_unique_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        job_title = d.pop("jobTitle", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        reference = d.pop("reference", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date,  Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()




        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, None, datetime.date]
        if _end_date is None:
            end_date = None
        elif isinstance(_end_date,  Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()




        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, RoleBasis]
        if isinstance(_basis,  Unset):
            basis = UNSET
        else:
            basis = RoleBasis(_basis)




        _type = d.pop("type", UNSET)
        type: Union[Unset, RoleType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = RoleType(_type)




        display_name = d.pop("displayName", UNSET)

        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, ContractPayOptionsBaseResponse]
        if isinstance(_pay_options,  Unset):
            pay_options = UNSET
        else:
            pay_options = ContractPayOptionsBaseResponse.from_dict(_pay_options)




        _working_pattern = d.pop("workingPattern", UNSET)
        working_pattern: Union[Unset, ContractWorkingPatternResponse]
        if isinstance(_working_pattern,  Unset):
            working_pattern = UNSET
        else:
            working_pattern = ContractWorkingPatternResponse.from_dict(_working_pattern)




        occupational_maternity_policy_unique_id = d.pop("occupationalMaternityPolicyUniqueId", UNSET)

        occupational_sickness_policy_unique_id = d.pop("occupationalSicknessPolicyUniqueId", UNSET)

        contract_employee_role_response = cls(
            id=id,
            job_title=job_title,
            is_primary=is_primary,
            reference=reference,
            start_date=start_date,
            end_date=end_date,
            basis=basis,
            type=type,
            display_name=display_name,
            pay_options=pay_options,
            working_pattern=working_pattern,
            occupational_maternity_policy_unique_id=occupational_maternity_policy_unique_id,
            occupational_sickness_policy_unique_id=occupational_sickness_policy_unique_id,
        )

        return contract_employee_role_response

