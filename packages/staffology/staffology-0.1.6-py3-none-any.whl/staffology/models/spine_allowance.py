import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.allowance_type import AllowanceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SpineAllowance")

@attr.s(auto_attribs=True)
class SpineAllowance:
    """
    Attributes:
        pay_spine_id (int): foreign key with pay spine table
        allowance_name (str): Name of Allowance
        pay_code_id (int): Pay Code Id for Spine Allowance
        allowance_effective_date (datetime.date): Allowance Effective Date
        allowance_type (Union[Unset, AllowanceType]):
        allowance_usual_annual_value (Union[Unset, None, float]): Value of Allowance Usual Annual
        allowance_range_lower_value (Union[Unset, None, float]): Value of Allowance Range Lower
        allowance_range_upper_value (Union[Unset, None, float]): Value of Allowance Range Upper
        allowance_always_fte (Union[Unset, bool]): Allowance Always FTE or Not
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    pay_spine_id: int
    allowance_name: str
    pay_code_id: int
    allowance_effective_date: datetime.date
    allowance_type: Union[Unset, AllowanceType] = UNSET
    allowance_usual_annual_value: Union[Unset, None, float] = UNSET
    allowance_range_lower_value: Union[Unset, None, float] = UNSET
    allowance_range_upper_value: Union[Unset, None, float] = UNSET
    allowance_always_fte: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pay_spine_id = self.pay_spine_id
        allowance_name = self.allowance_name
        pay_code_id = self.pay_code_id
        allowance_effective_date = self.allowance_effective_date.isoformat() 
        allowance_type: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_type, Unset):
            allowance_type = self.allowance_type.value

        allowance_usual_annual_value = self.allowance_usual_annual_value
        allowance_range_lower_value = self.allowance_range_lower_value
        allowance_range_upper_value = self.allowance_range_upper_value
        allowance_always_fte = self.allowance_always_fte
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "paySpineId": pay_spine_id,
            "allowanceName": allowance_name,
            "payCodeId": pay_code_id,
            "allowanceEffectiveDate": allowance_effective_date,
        })
        if allowance_type is not UNSET:
            field_dict["allowanceType"] = allowance_type
        if allowance_usual_annual_value is not UNSET:
            field_dict["allowanceUsualAnnualValue"] = allowance_usual_annual_value
        if allowance_range_lower_value is not UNSET:
            field_dict["allowanceRangeLowerValue"] = allowance_range_lower_value
        if allowance_range_upper_value is not UNSET:
            field_dict["allowanceRangeUpperValue"] = allowance_range_upper_value
        if allowance_always_fte is not UNSET:
            field_dict["allowanceAlwaysFTE"] = allowance_always_fte
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_spine_id = d.pop("paySpineId")

        allowance_name = d.pop("allowanceName")

        pay_code_id = d.pop("payCodeId")

        allowance_effective_date = isoparse(d.pop("allowanceEffectiveDate")).date()




        _allowance_type = d.pop("allowanceType", UNSET)
        allowance_type: Union[Unset, AllowanceType]
        if isinstance(_allowance_type,  Unset):
            allowance_type = UNSET
        else:
            allowance_type = AllowanceType(_allowance_type)




        allowance_usual_annual_value = d.pop("allowanceUsualAnnualValue", UNSET)

        allowance_range_lower_value = d.pop("allowanceRangeLowerValue", UNSET)

        allowance_range_upper_value = d.pop("allowanceRangeUpperValue", UNSET)

        allowance_always_fte = d.pop("allowanceAlwaysFTE", UNSET)

        id = d.pop("id", UNSET)

        spine_allowance = cls(
            pay_spine_id=pay_spine_id,
            allowance_name=allowance_name,
            pay_code_id=pay_code_id,
            allowance_effective_date=allowance_effective_date,
            allowance_type=allowance_type,
            allowance_usual_annual_value=allowance_usual_annual_value,
            allowance_range_lower_value=allowance_range_lower_value,
            allowance_range_upper_value=allowance_range_upper_value,
            allowance_always_fte=allowance_always_fte,
            id=id,
        )

        return spine_allowance

