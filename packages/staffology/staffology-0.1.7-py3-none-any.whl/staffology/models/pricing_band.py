from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PricingBand")

@attr.s(auto_attribs=True)
class PricingBand:
    """
    Attributes:
        description (Union[Unset, None, str]):
        from_ (Union[Unset, int]):
        to (Union[Unset, int]):
        price (Union[Unset, float]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    description: Union[Unset, None, str] = UNSET
    from_: Union[Unset, int] = UNSET
    to: Union[Unset, int] = UNSET
    price: Union[Unset, float] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        from_ = self.from_
        to = self.to
        price = self.price
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if price is not UNSET:
            field_dict["price"] = price
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        from_ = d.pop("from", UNSET)

        to = d.pop("to", UNSET)

        price = d.pop("price", UNSET)

        id = d.pop("id", UNSET)

        pricing_band = cls(
            description=description,
            from_=from_,
            to=to,
            price=price,
            id=id,
        )

        return pricing_band

