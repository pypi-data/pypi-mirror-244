import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.allowance_type import AllowanceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractSpineAllowanceRequest")

@attr.s(auto_attribs=True)
class ContractSpineAllowanceRequest:
    """
    Attributes:
        allowance_name (Union[Unset, None, str]): Name of Allowance
        pay_code_id (Union[Unset, int]): Pay Code Id for Spine Allowance
        allowance_type (Union[Unset, AllowanceType]):
        allowance_usual_annual_value (Union[Unset, float]): Value of Allowance Usual Annual
        allowance_range_lower_value (Union[Unset, float]): Value of Allowance Range Lower
        allowance_range_upper_value (Union[Unset, float]): Value of Allowance Range Upper
        allowance_effective_date (Union[Unset, datetime.date]): Allowance Effective Date
        allowance_always_fte (Union[Unset, bool]): Allowance Always FTE or Not
    """

    allowance_name: Union[Unset, None, str] = UNSET
    pay_code_id: Union[Unset, int] = UNSET
    allowance_type: Union[Unset, AllowanceType] = UNSET
    allowance_usual_annual_value: Union[Unset, float] = UNSET
    allowance_range_lower_value: Union[Unset, float] = UNSET
    allowance_range_upper_value: Union[Unset, float] = UNSET
    allowance_effective_date: Union[Unset, datetime.date] = UNSET
    allowance_always_fte: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        allowance_name = self.allowance_name
        pay_code_id = self.pay_code_id
        allowance_type: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_type, Unset):
            allowance_type = self.allowance_type.value

        allowance_usual_annual_value = self.allowance_usual_annual_value
        allowance_range_lower_value = self.allowance_range_lower_value
        allowance_range_upper_value = self.allowance_range_upper_value
        allowance_effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_effective_date, Unset):
            allowance_effective_date = self.allowance_effective_date.isoformat()

        allowance_always_fte = self.allowance_always_fte

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if allowance_name is not UNSET:
            field_dict["allowanceName"] = allowance_name
        if pay_code_id is not UNSET:
            field_dict["payCodeId"] = pay_code_id
        if allowance_type is not UNSET:
            field_dict["allowanceType"] = allowance_type
        if allowance_usual_annual_value is not UNSET:
            field_dict["allowanceUsualAnnualValue"] = allowance_usual_annual_value
        if allowance_range_lower_value is not UNSET:
            field_dict["allowanceRangeLowerValue"] = allowance_range_lower_value
        if allowance_range_upper_value is not UNSET:
            field_dict["allowanceRangeUpperValue"] = allowance_range_upper_value
        if allowance_effective_date is not UNSET:
            field_dict["allowanceEffectiveDate"] = allowance_effective_date
        if allowance_always_fte is not UNSET:
            field_dict["allowanceAlwaysFTE"] = allowance_always_fte

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allowance_name = d.pop("allowanceName", UNSET)

        pay_code_id = d.pop("payCodeId", UNSET)

        _allowance_type = d.pop("allowanceType", UNSET)
        allowance_type: Union[Unset, AllowanceType]
        if isinstance(_allowance_type,  Unset):
            allowance_type = UNSET
        else:
            allowance_type = AllowanceType(_allowance_type)




        allowance_usual_annual_value = d.pop("allowanceUsualAnnualValue", UNSET)

        allowance_range_lower_value = d.pop("allowanceRangeLowerValue", UNSET)

        allowance_range_upper_value = d.pop("allowanceRangeUpperValue", UNSET)

        _allowance_effective_date = d.pop("allowanceEffectiveDate", UNSET)
        allowance_effective_date: Union[Unset, datetime.date]
        if isinstance(_allowance_effective_date,  Unset):
            allowance_effective_date = UNSET
        else:
            allowance_effective_date = isoparse(_allowance_effective_date).date()




        allowance_always_fte = d.pop("allowanceAlwaysFTE", UNSET)

        contract_spine_allowance_request = cls(
            allowance_name=allowance_name,
            pay_code_id=pay_code_id,
            allowance_type=allowance_type,
            allowance_usual_annual_value=allowance_usual_annual_value,
            allowance_range_lower_value=allowance_range_lower_value,
            allowance_range_upper_value=allowance_range_upper_value,
            allowance_effective_date=allowance_effective_date,
            allowance_always_fte=allowance_always_fte,
        )

        return contract_spine_allowance_request

