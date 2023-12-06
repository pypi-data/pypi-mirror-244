from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractNetOfOnCostsSimulationResponse")

@attr.s(auto_attribs=True)
class ContractNetOfOnCostsSimulationResponse:
    """
    Attributes:
        gross_pay (Union[Unset, float]):
        employee_pension (Union[Unset, float]):
        tax_due (Union[Unset, float]):
        ni_due (Union[Unset, float]):
        net_pay (Union[Unset, float]):
    """

    gross_pay: Union[Unset, float] = UNSET
    employee_pension: Union[Unset, float] = UNSET
    tax_due: Union[Unset, float] = UNSET
    ni_due: Union[Unset, float] = UNSET
    net_pay: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        gross_pay = self.gross_pay
        employee_pension = self.employee_pension
        tax_due = self.tax_due
        ni_due = self.ni_due
        net_pay = self.net_pay

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if gross_pay is not UNSET:
            field_dict["grossPay"] = gross_pay
        if employee_pension is not UNSET:
            field_dict["employeePension"] = employee_pension
        if tax_due is not UNSET:
            field_dict["taxDue"] = tax_due
        if ni_due is not UNSET:
            field_dict["niDue"] = ni_due
        if net_pay is not UNSET:
            field_dict["netPay"] = net_pay

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        gross_pay = d.pop("grossPay", UNSET)

        employee_pension = d.pop("employeePension", UNSET)

        tax_due = d.pop("taxDue", UNSET)

        ni_due = d.pop("niDue", UNSET)

        net_pay = d.pop("netPay", UNSET)

        contract_net_of_on_costs_simulation_response = cls(
            gross_pay=gross_pay,
            employee_pension=employee_pension,
            tax_due=tax_due,
            ni_due=ni_due,
            net_pay=net_pay,
        )

        return contract_net_of_on_costs_simulation_response

