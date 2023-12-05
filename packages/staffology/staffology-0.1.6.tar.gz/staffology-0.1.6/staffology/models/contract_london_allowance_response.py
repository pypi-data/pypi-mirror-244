from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.london_allowance_type import LondonAllowanceType
from ..models.london_allowance_value_type import LondonAllowanceValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractLondonAllowanceResponse")

@attr.s(auto_attribs=True)
class ContractLondonAllowanceResponse:
    """
    Attributes:
        type (Union[Unset, LondonAllowanceType]):
        value_type (Union[Unset, LondonAllowanceValueType]):
        value (Union[Unset, float]): Value of London Allowance
        unique_id (Union[Unset, str]): London Allowance identifier
    """

    type: Union[Unset, LondonAllowanceType] = UNSET
    value_type: Union[Unset, LondonAllowanceValueType] = UNSET
    value: Union[Unset, float] = UNSET
    unique_id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        value = self.value
        unique_id = self.unique_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if type is not UNSET:
            field_dict["type"] = type
        if value_type is not UNSET:
            field_dict["valueType"] = value_type
        if value is not UNSET:
            field_dict["value"] = value
        if unique_id is not UNSET:
            field_dict["uniqueId"] = unique_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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

        unique_id = d.pop("uniqueId", UNSET)

        contract_london_allowance_response = cls(
            type=type,
            value_type=value_type,
            value=value,
            unique_id=unique_id,
        )

        return contract_london_allowance_response

