from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeRolePayItem")

@attr.s(auto_attribs=True)
class EmployeeRolePayItem:
    """
    Attributes:
        role_id (Union[Unset, str]):
        is_primary (Union[Unset, bool]):
        base_daily_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base daily rate. Eg sick.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        base_hourly_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base hourly rate. Eg Overtime.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        weight (Union[Unset, float]): This property is used to calculate values for the relative weight of the usual pay
            for
            each role compared to the sum of all roles' usual pay
            Usual pay for the purpose of the current value's calculation is based on the employee's permanent pay items
            including employee basic pay and permanent addition and deduction pay lines subject to NI or Tax
    """

    role_id: Union[Unset, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    base_daily_rate: Union[Unset, float] = UNSET
    base_hourly_rate: Union[Unset, float] = UNSET
    weight: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        role_id = self.role_id
        is_primary = self.is_primary
        base_daily_rate = self.base_daily_rate
        base_hourly_rate = self.base_hourly_rate
        weight = self.weight

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if role_id is not UNSET:
            field_dict["roleId"] = role_id
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary
        if base_daily_rate is not UNSET:
            field_dict["baseDailyRate"] = base_daily_rate
        if base_hourly_rate is not UNSET:
            field_dict["baseHourlyRate"] = base_hourly_rate
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role_id = d.pop("roleId", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        base_daily_rate = d.pop("baseDailyRate", UNSET)

        base_hourly_rate = d.pop("baseHourlyRate", UNSET)

        weight = d.pop("weight", UNSET)

        employee_role_pay_item = cls(
            role_id=role_id,
            is_primary=is_primary,
            base_daily_rate=base_daily_rate,
            base_hourly_rate=base_hourly_rate,
            weight=weight,
        )

        return employee_role_pay_item

