from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionOpeningBalances")

@attr.s(auto_attribs=True)
class PensionOpeningBalances:
    """
    Attributes:
        pensionable_earnings (Union[Unset, float]): Opening balances for pensionable earnings
        pensionable_pay (Union[Unset, float]): Opening balances for pensionable pay
        employee_pension_contribution (Union[Unset, float]): Opening balances for employee pension contribution
        employee_pension_contribution_avc (Union[Unset, float]): Opening balances for employee pension contribution avc
        employer_pension_contribution (Union[Unset, float]): Opening balances for employer pension contribution
        assumed_pensionable_pay (Union[Unset, float]): Opening balances for assumed pensionable pay
    """

    pensionable_earnings: Union[Unset, float] = UNSET
    pensionable_pay: Union[Unset, float] = UNSET
    employee_pension_contribution: Union[Unset, float] = UNSET
    employee_pension_contribution_avc: Union[Unset, float] = UNSET
    employer_pension_contribution: Union[Unset, float] = UNSET
    assumed_pensionable_pay: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pensionable_earnings = self.pensionable_earnings
        pensionable_pay = self.pensionable_pay
        employee_pension_contribution = self.employee_pension_contribution
        employee_pension_contribution_avc = self.employee_pension_contribution_avc
        employer_pension_contribution = self.employer_pension_contribution
        assumed_pensionable_pay = self.assumed_pensionable_pay

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pensionable_earnings is not UNSET:
            field_dict["pensionableEarnings"] = pensionable_earnings
        if pensionable_pay is not UNSET:
            field_dict["pensionablePay"] = pensionable_pay
        if employee_pension_contribution is not UNSET:
            field_dict["employeePensionContribution"] = employee_pension_contribution
        if employee_pension_contribution_avc is not UNSET:
            field_dict["employeePensionContributionAvc"] = employee_pension_contribution_avc
        if employer_pension_contribution is not UNSET:
            field_dict["employerPensionContribution"] = employer_pension_contribution
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pensionable_earnings = d.pop("pensionableEarnings", UNSET)

        pensionable_pay = d.pop("pensionablePay", UNSET)

        employee_pension_contribution = d.pop("employeePensionContribution", UNSET)

        employee_pension_contribution_avc = d.pop("employeePensionContributionAvc", UNSET)

        employer_pension_contribution = d.pop("employerPensionContribution", UNSET)

        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        pension_opening_balances = cls(
            pensionable_earnings=pensionable_earnings,
            pensionable_pay=pensionable_pay,
            employee_pension_contribution=employee_pension_contribution,
            employee_pension_contribution_avc=employee_pension_contribution_avc,
            employer_pension_contribution=employer_pension_contribution,
            assumed_pensionable_pay=assumed_pensionable_pay,
        )

        return pension_opening_balances

