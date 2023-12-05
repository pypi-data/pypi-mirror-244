from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.london_allowance_type import LondonAllowanceType
from ..models.london_allowance_value_type import LondonAllowanceValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LondonAllowance")

@attr.s(auto_attribs=True)
class LondonAllowance:
    """
    Attributes:
        pay_spine_id (int): foreign key with pay spine table
        type (Union[Unset, LondonAllowanceType]):
        value_type (Union[Unset, LondonAllowanceValueType]):
        value (Union[Unset, float]): Value of London Allowance
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    pay_spine_id: int
    type: Union[Unset, LondonAllowanceType] = UNSET
    value_type: Union[Unset, LondonAllowanceValueType] = UNSET
    value: Union[Unset, float] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pay_spine_id = self.pay_spine_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        value = self.value
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "paySpineId": pay_spine_id,
        })
        if type is not UNSET:
            field_dict["type"] = type
        if value_type is not UNSET:
            field_dict["valueType"] = value_type
        if value is not UNSET:
            field_dict["value"] = value
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_spine_id = d.pop("paySpineId")

        _type = d.pop("type", UNSET)
        type: Union[Unset, LondonAllowanceType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = LondonAllowanceType(_type)




        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, LondonAllowanceValueType]
        if isinstance(_value_type,  Unset):
            value_type = UNSET
        else:
            value_type = LondonAllowanceValueType(_value_type)




        value = d.pop("value", UNSET)

        id = d.pop("id", UNSET)

        london_allowance = cls(
            pay_spine_id=pay_spine_id,
            type=type,
            value_type=value_type,
            value=value,
            id=id,
        )

        return london_allowance

