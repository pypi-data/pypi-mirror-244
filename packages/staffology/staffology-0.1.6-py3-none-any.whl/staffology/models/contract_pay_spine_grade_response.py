import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPaySpineGradeResponse")

@attr.s(auto_attribs=True)
class ContractPaySpineGradeResponse:
    """
    Attributes:
        name (Union[Unset, None, str]): Pay spine grade name
        lower_point_unique_id (Union[Unset, str]): Id of lower spinal point used.
        upper_point_unique_id (Union[Unset, str]): Id of upper spinal point used.
        upper_point_use_max (Union[Unset, bool]): Use the Alt Max Value of the Upper Point. (Default false)
        effective_date (Union[Unset, datetime.date]): Date that this configuration is effective from.
        unique_id (Union[Unset, str]): Pay spine grade Id
    """

    name: Union[Unset, None, str] = UNSET
    lower_point_unique_id: Union[Unset, str] = UNSET
    upper_point_unique_id: Union[Unset, str] = UNSET
    upper_point_use_max: Union[Unset, bool] = UNSET
    effective_date: Union[Unset, datetime.date] = UNSET
    unique_id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        lower_point_unique_id = self.lower_point_unique_id
        upper_point_unique_id = self.upper_point_unique_id
        upper_point_use_max = self.upper_point_use_max
        effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        unique_id = self.unique_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if lower_point_unique_id is not UNSET:
            field_dict["lowerPointUniqueId"] = lower_point_unique_id
        if upper_point_unique_id is not UNSET:
            field_dict["upperPointUniqueId"] = upper_point_unique_id
        if upper_point_use_max is not UNSET:
            field_dict["upperPointUseMax"] = upper_point_use_max
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date
        if unique_id is not UNSET:
            field_dict["uniqueId"] = unique_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        lower_point_unique_id = d.pop("lowerPointUniqueId", UNSET)

        upper_point_unique_id = d.pop("upperPointUniqueId", UNSET)

        upper_point_use_max = d.pop("upperPointUseMax", UNSET)

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: Union[Unset, datetime.date]
        if isinstance(_effective_date,  Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date).date()




        unique_id = d.pop("uniqueId", UNSET)

        contract_pay_spine_grade_response = cls(
            name=name,
            lower_point_unique_id=lower_point_unique_id,
            upper_point_unique_id=upper_point_unique_id,
            upper_point_use_max=upper_point_use_max,
            effective_date=effective_date,
            unique_id=unique_id,
        )

        return contract_pay_spine_grade_response

