import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.employee_role_pay_options import EmployeeRolePayOptions
from ..models.item import Item
from ..models.role_basis import RoleBasis
from ..models.role_type import RoleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeRole")

@attr.s(auto_attribs=True)
class EmployeeRole:
    """
    Attributes:
        job_title (Union[Unset, None, str]): Job Title of the Role
        is_primary (Union[Unset, bool]): Set to True if this is Primary role of the Employee
        reference (Union[Unset, None, str]):
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, None, datetime.date]):
        basis (Union[Unset, RoleBasis]):
        type (Union[Unset, RoleType]):
        pay_options (Union[Unset, EmployeeRolePayOptions]):
        working_pattern_id (Union[Unset, None, str]): Used when calculating payments for Leave.
            If null then the default Working Pattern is used
        occupational_maternity_policy_unique_id (Union[Unset, None, str]): Used for assigning occupational maternity
            policy
        occupational_sickness_policy_unique_id (Union[Unset, None, str]): Used for assigning occupational sickness
            policy
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    job_title: Union[Unset, None, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    reference: Union[Unset, None, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, None, datetime.date] = UNSET
    basis: Union[Unset, RoleBasis] = UNSET
    type: Union[Unset, RoleType] = UNSET
    pay_options: Union[Unset, EmployeeRolePayOptions] = UNSET
    working_pattern_id: Union[Unset, None, str] = UNSET
    occupational_maternity_policy_unique_id: Union[Unset, None, str] = UNSET
    occupational_sickness_policy_unique_id: Union[Unset, None, str] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
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

        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        working_pattern_id = self.working_pattern_id
        occupational_maternity_policy_unique_id = self.occupational_maternity_policy_unique_id
        occupational_sickness_policy_unique_id = self.occupational_sickness_policy_unique_id
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
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
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options
        if working_pattern_id is not UNSET:
            field_dict["workingPatternId"] = working_pattern_id
        if occupational_maternity_policy_unique_id is not UNSET:
            field_dict["occupationalMaternityPolicyUniqueId"] = occupational_maternity_policy_unique_id
        if occupational_sickness_policy_unique_id is not UNSET:
            field_dict["occupationalSicknessPolicyUniqueId"] = occupational_sickness_policy_unique_id
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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




        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, EmployeeRolePayOptions]
        if isinstance(_pay_options,  Unset):
            pay_options = UNSET
        else:
            pay_options = EmployeeRolePayOptions.from_dict(_pay_options)




        working_pattern_id = d.pop("workingPatternId", UNSET)

        occupational_maternity_policy_unique_id = d.pop("occupationalMaternityPolicyUniqueId", UNSET)

        occupational_sickness_policy_unique_id = d.pop("occupationalSicknessPolicyUniqueId", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        id = d.pop("id", UNSET)

        employee_role = cls(
            job_title=job_title,
            is_primary=is_primary,
            reference=reference,
            start_date=start_date,
            end_date=end_date,
            basis=basis,
            type=type,
            pay_options=pay_options,
            working_pattern_id=working_pattern_id,
            occupational_maternity_policy_unique_id=occupational_maternity_policy_unique_id,
            occupational_sickness_policy_unique_id=occupational_sickness_policy_unique_id,
            employee=employee,
            id=id,
        )

        return employee_role

