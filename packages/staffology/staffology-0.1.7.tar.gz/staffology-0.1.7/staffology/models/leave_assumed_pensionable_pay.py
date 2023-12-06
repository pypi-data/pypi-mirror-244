from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LeaveAssumedPensionablePay")

@attr.s(auto_attribs=True)
class LeaveAssumedPensionablePay:
    """
    Attributes:
        role_reference (Union[Unset, None, str]): Employee role reference
        role_id (Union[Unset, str]): Employee role unique Id
        is_primary (Union[Unset, bool]): Boolean flag indicates if the role is primary
        assumed_pensionable_pay (Union[Unset, None, float]): Assumed Pensionable Pay (APP) is an average figure,
            calculated as the average pay in the 3 months
            (or 12 weeks if weekly/fortnightly/fourweekly paid) before the absence
        automatic_app_calculation (Union[Unset, bool]): If set to True then we'll automatically calculate the
            AssumedPensionablePay.
            Set it to false if you want to manually provide a figure that overrides our calculations
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    role_reference: Union[Unset, None, str] = UNSET
    role_id: Union[Unset, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    assumed_pensionable_pay: Union[Unset, None, float] = UNSET
    automatic_app_calculation: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        role_reference = self.role_reference
        role_id = self.role_id
        is_primary = self.is_primary
        assumed_pensionable_pay = self.assumed_pensionable_pay
        automatic_app_calculation = self.automatic_app_calculation
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if role_reference is not UNSET:
            field_dict["roleReference"] = role_reference
        if role_id is not UNSET:
            field_dict["roleId"] = role_id
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if automatic_app_calculation is not UNSET:
            field_dict["automaticAPPCalculation"] = automatic_app_calculation
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role_reference = d.pop("roleReference", UNSET)

        role_id = d.pop("roleId", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        automatic_app_calculation = d.pop("automaticAPPCalculation", UNSET)

        id = d.pop("id", UNSET)

        leave_assumed_pensionable_pay = cls(
            role_reference=role_reference,
            role_id=role_id,
            is_primary=is_primary,
            assumed_pensionable_pay=assumed_pensionable_pay,
            automatic_app_calculation=automatic_app_calculation,
            id=id,
        )

        return leave_assumed_pensionable_pay

