from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NiYtdValue")

@attr.s(auto_attribs=True)
class NiYtdValue:
    """
    Attributes:
        type (Union[Unset, None, str]):
        brought_forward (Union[Unset, float]):
        period (Union[Unset, float]):
        value (Union[Unset, float]):
    """

    type: Union[Unset, None, str] = UNSET
    brought_forward: Union[Unset, float] = UNSET
    period: Union[Unset, float] = UNSET
    value: Union[Unset, float] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        brought_forward = self.brought_forward
        period = self.period
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if type is not UNSET:
            field_dict["type"] = type
        if brought_forward is not UNSET:
            field_dict["broughtForward"] = brought_forward
        if period is not UNSET:
            field_dict["period"] = period
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        brought_forward = d.pop("broughtForward", UNSET)

        period = d.pop("period", UNSET)

        value = d.pop("value", UNSET)

        ni_ytd_value = cls(
            type=type,
            brought_forward=brought_forward,
            period=period,
            value=value,
        )

        return ni_ytd_value

