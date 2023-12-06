from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_basis import PayBasis
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeePay")

@attr.s(auto_attribs=True)
class PapdisEmployeePay:
    """
    Attributes:
        pensionable_earnings_amount (Union[Unset, float]): [readonly]
        total_gross_qualifying_earnings_amount (Union[Unset, float]): [readonly]
        annual_salary (Union[Unset, float]): [readonly]
        annual_pensionable_earnings_amount (Union[Unset, float]): [readonly]
        basis (Union[Unset, PayBasis]):
        pay_amount_multiplier (Union[Unset, None, float]): [readonly]
    """

    pensionable_earnings_amount: Union[Unset, float] = UNSET
    total_gross_qualifying_earnings_amount: Union[Unset, float] = UNSET
    annual_salary: Union[Unset, float] = UNSET
    annual_pensionable_earnings_amount: Union[Unset, float] = UNSET
    basis: Union[Unset, PayBasis] = UNSET
    pay_amount_multiplier: Union[Unset, None, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pensionable_earnings_amount = self.pensionable_earnings_amount
        total_gross_qualifying_earnings_amount = self.total_gross_qualifying_earnings_amount
        annual_salary = self.annual_salary
        annual_pensionable_earnings_amount = self.annual_pensionable_earnings_amount
        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        pay_amount_multiplier = self.pay_amount_multiplier

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pensionable_earnings_amount is not UNSET:
            field_dict["pensionableEarningsAmount"] = pensionable_earnings_amount
        if total_gross_qualifying_earnings_amount is not UNSET:
            field_dict["totalGrossQualifyingEarningsAmount"] = total_gross_qualifying_earnings_amount
        if annual_salary is not UNSET:
            field_dict["annualSalary"] = annual_salary
        if annual_pensionable_earnings_amount is not UNSET:
            field_dict["annualPensionableEarningsAmount"] = annual_pensionable_earnings_amount
        if basis is not UNSET:
            field_dict["basis"] = basis
        if pay_amount_multiplier is not UNSET:
            field_dict["payAmountMultiplier"] = pay_amount_multiplier

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pensionable_earnings_amount = d.pop("pensionableEarningsAmount", UNSET)

        total_gross_qualifying_earnings_amount = d.pop("totalGrossQualifyingEarningsAmount", UNSET)

        annual_salary = d.pop("annualSalary", UNSET)

        annual_pensionable_earnings_amount = d.pop("annualPensionableEarningsAmount", UNSET)

        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, PayBasis]
        if isinstance(_basis,  Unset):
            basis = UNSET
        else:
            basis = PayBasis(_basis)




        pay_amount_multiplier = d.pop("payAmountMultiplier", UNSET)

        papdis_employee_pay = cls(
            pensionable_earnings_amount=pensionable_earnings_amount,
            total_gross_qualifying_earnings_amount=total_gross_qualifying_earnings_amount,
            annual_salary=annual_salary,
            annual_pensionable_earnings_amount=annual_pensionable_earnings_amount,
            basis=basis,
            pay_amount_multiplier=pay_amount_multiplier,
        )

        return papdis_employee_pay

