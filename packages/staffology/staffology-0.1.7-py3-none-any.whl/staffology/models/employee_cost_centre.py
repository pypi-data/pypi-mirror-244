from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeCostCentre")

@attr.s(auto_attribs=True)
class EmployeeCostCentre:
    """Used to represent an Employees membership of a Cost Centre

    Attributes:
        code (str): The Code for the Cost Centre
        color (Union[Unset, None, str]): [readonly] The Color for the Cost Centre
        title (Union[Unset, None, str]): [readonly] The Title for the Cost Centre
        is_primary (Union[Unset, bool]): Set to true if this is the primary Cost Centre for the Employee.
            Only one Cost Centre can be set as the primary.
        weighting (Union[Unset, float]): If there is more than one Cost Centre Membership for the Employee then this
            determines the weighting to give to this membership.
            ie, if he is in two Cost Centre you might set the primary as 0.8 and the secondary as 0.2;
        employee (Union[Unset, Item]):
    """

    code: str
    color: Union[Unset, None, str] = UNSET
    title: Union[Unset, None, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    weighting: Union[Unset, float] = UNSET
    employee: Union[Unset, Item] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        color = self.color
        title = self.title
        is_primary = self.is_primary
        weighting = self.weighting
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "code": code,
        })
        if color is not UNSET:
            field_dict["color"] = color
        if title is not UNSET:
            field_dict["title"] = title
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary
        if weighting is not UNSET:
            field_dict["weighting"] = weighting
        if employee is not UNSET:
            field_dict["employee"] = employee

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        color = d.pop("color", UNSET)

        title = d.pop("title", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        weighting = d.pop("weighting", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        employee_cost_centre = cls(
            code=code,
            color=color,
            title=title,
            is_primary=is_primary,
            weighting=weighting,
            employee=employee,
        )

        return employee_cost_centre

