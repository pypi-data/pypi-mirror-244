from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitlementBand")

@attr.s(auto_attribs=True)
class EntitlementBand:
    """
    Attributes:
        percent_of_pay (Union[Unset, float]):
        period (Union[Unset, int]):
        pay_ssp_in_addition (Union[Unset, bool]):
        order (Union[Unset, int]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    percent_of_pay: Union[Unset, float] = UNSET
    period: Union[Unset, int] = UNSET
    pay_ssp_in_addition: Union[Unset, bool] = UNSET
    order: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        percent_of_pay = self.percent_of_pay
        period = self.period
        pay_ssp_in_addition = self.pay_ssp_in_addition
        order = self.order
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if percent_of_pay is not UNSET:
            field_dict["percentOfPay"] = percent_of_pay
        if period is not UNSET:
            field_dict["period"] = period
        if pay_ssp_in_addition is not UNSET:
            field_dict["paySspInAddition"] = pay_ssp_in_addition
        if order is not UNSET:
            field_dict["order"] = order
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        percent_of_pay = d.pop("percentOfPay", UNSET)

        period = d.pop("period", UNSET)

        pay_ssp_in_addition = d.pop("paySspInAddition", UNSET)

        order = d.pop("order", UNSET)

        id = d.pop("id", UNSET)

        entitlement_band = cls(
            percent_of_pay=percent_of_pay,
            period=period,
            pay_ssp_in_addition=pay_ssp_in_addition,
            order=order,
            id=id,
        )

        return entitlement_band

