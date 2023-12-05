from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeFlexibleDrawdown")

@attr.s(auto_attribs=True)
class FpsEmployeeFlexibleDrawdown:
    """
    Attributes:
        flexibly_accessing_pension_rights (Union[Unset, None, str]):
        pension_death_benefit (Union[Unset, None, str]):
        serious_ill_health_lump_sum (Union[Unset, None, str]):
        taxable_payment (Union[Unset, None, str]):
        nontaxable_payment (Union[Unset, None, str]):
    """

    flexibly_accessing_pension_rights: Union[Unset, None, str] = UNSET
    pension_death_benefit: Union[Unset, None, str] = UNSET
    serious_ill_health_lump_sum: Union[Unset, None, str] = UNSET
    taxable_payment: Union[Unset, None, str] = UNSET
    nontaxable_payment: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        flexibly_accessing_pension_rights = self.flexibly_accessing_pension_rights
        pension_death_benefit = self.pension_death_benefit
        serious_ill_health_lump_sum = self.serious_ill_health_lump_sum
        taxable_payment = self.taxable_payment
        nontaxable_payment = self.nontaxable_payment

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if flexibly_accessing_pension_rights is not UNSET:
            field_dict["flexiblyAccessingPensionRights"] = flexibly_accessing_pension_rights
        if pension_death_benefit is not UNSET:
            field_dict["pensionDeathBenefit"] = pension_death_benefit
        if serious_ill_health_lump_sum is not UNSET:
            field_dict["seriousIllHealthLumpSum"] = serious_ill_health_lump_sum
        if taxable_payment is not UNSET:
            field_dict["taxablePayment"] = taxable_payment
        if nontaxable_payment is not UNSET:
            field_dict["nontaxablePayment"] = nontaxable_payment

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        flexibly_accessing_pension_rights = d.pop("flexiblyAccessingPensionRights", UNSET)

        pension_death_benefit = d.pop("pensionDeathBenefit", UNSET)

        serious_ill_health_lump_sum = d.pop("seriousIllHealthLumpSum", UNSET)

        taxable_payment = d.pop("taxablePayment", UNSET)

        nontaxable_payment = d.pop("nontaxablePayment", UNSET)

        fps_employee_flexible_drawdown = cls(
            flexibly_accessing_pension_rights=flexibly_accessing_pension_rights,
            pension_death_benefit=pension_death_benefit,
            serious_ill_health_lump_sum=serious_ill_health_lump_sum,
            taxable_payment=taxable_payment,
            nontaxable_payment=nontaxable_payment,
        )

        return fps_employee_flexible_drawdown

