from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionRefund")

@attr.s(auto_attribs=True)
class PensionRefund:
    """Used to represent a Pension Refund

    Attributes:
        employee_refund (float):
        employer_refund (float):
        pension_scheme_unique_id (Union[Unset, str]):
        pension_unique_id (Union[Unset, str]):
        pay_in_current_pay_run (Union[Unset, bool]):
        pay_run (Union[Unset, Item]):
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    employee_refund: float
    employer_refund: float
    pension_scheme_unique_id: Union[Unset, str] = UNSET
    pension_unique_id: Union[Unset, str] = UNSET
    pay_in_current_pay_run: Union[Unset, bool] = UNSET
    pay_run: Union[Unset, Item] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        employee_refund = self.employee_refund
        employer_refund = self.employer_refund
        pension_scheme_unique_id = self.pension_scheme_unique_id
        pension_unique_id = self.pension_unique_id
        pay_in_current_pay_run = self.pay_in_current_pay_run
        pay_run: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_run, Unset):
            pay_run = self.pay_run.to_dict()

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "employeeRefund": employee_refund,
            "employerRefund": employer_refund,
        })
        if pension_scheme_unique_id is not UNSET:
            field_dict["pensionSchemeUniqueId"] = pension_scheme_unique_id
        if pension_unique_id is not UNSET:
            field_dict["pensionUniqueId"] = pension_unique_id
        if pay_in_current_pay_run is not UNSET:
            field_dict["payInCurrentPayRun"] = pay_in_current_pay_run
        if pay_run is not UNSET:
            field_dict["payRun"] = pay_run
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_refund = d.pop("employeeRefund")

        employer_refund = d.pop("employerRefund")

        pension_scheme_unique_id = d.pop("pensionSchemeUniqueId", UNSET)

        pension_unique_id = d.pop("pensionUniqueId", UNSET)

        pay_in_current_pay_run = d.pop("payInCurrentPayRun", UNSET)

        _pay_run = d.pop("payRun", UNSET)
        pay_run: Union[Unset, Item]
        if isinstance(_pay_run,  Unset):
            pay_run = UNSET
        else:
            pay_run = Item.from_dict(_pay_run)




        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee,  Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)




        id = d.pop("id", UNSET)

        pension_refund = cls(
            employee_refund=employee_refund,
            employer_refund=employer_refund,
            pension_scheme_unique_id=pension_scheme_unique_id,
            pension_unique_id=pension_unique_id,
            pay_in_current_pay_run=pay_in_current_pay_run,
            pay_run=pay_run,
            employee=employee,
            id=id,
        )

        return pension_refund

