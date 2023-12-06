from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenefitPayrolled")

@attr.s(auto_attribs=True)
class BenefitPayrolled:
    """
    Attributes:
        tax_year (Union[Unset, TaxYear]):
        amount (Union[Unset, float]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    amount: Union[Unset, float] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        amount = self.amount
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if amount is not UNSET:
            field_dict["amount"] = amount
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year,  Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)




        amount = d.pop("amount", UNSET)

        id = d.pop("id", UNSET)

        benefit_payrolled = cls(
            tax_year=tax_year,
            amount=amount,
            id=id,
        )

        return benefit_payrolled

