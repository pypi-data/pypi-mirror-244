from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractDepartmentResponse")

@attr.s(auto_attribs=True)
class ContractDepartmentResponse:
    """
    Attributes:
        code (str): The unique code for this Department
        title (str): The name of this Department
        employee_count (Union[Unset, int]): The number of employees with this set as their primary department
        color (Union[Unset, None, str]): A color to used to represent this Department, in hex format. ie 'ff0000'
        accounting_code (Union[Unset, None, str]):
    """

    code: str
    title: str
    employee_count: Union[Unset, int] = UNSET
    color: Union[Unset, None, str] = UNSET
    accounting_code: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        title = self.title
        employee_count = self.employee_count
        color = self.color
        accounting_code = self.accounting_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "code": code,
            "title": title,
        })
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if color is not UNSET:
            field_dict["color"] = color
        if accounting_code is not UNSET:
            field_dict["accountingCode"] = accounting_code

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        title = d.pop("title")

        employee_count = d.pop("employeeCount", UNSET)

        color = d.pop("color", UNSET)

        accounting_code = d.pop("accountingCode", UNSET)

        contract_department_response = cls(
            code=code,
            title=title,
            employee_count=employee_count,
            color=color,
            accounting_code=accounting_code,
        )

        return contract_department_response

