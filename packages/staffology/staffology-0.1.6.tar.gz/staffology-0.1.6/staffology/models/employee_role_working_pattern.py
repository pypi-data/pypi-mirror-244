import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeRoleWorkingPattern")

@attr.s(auto_attribs=True)
class EmployeeRoleWorkingPattern:
    """Used to represent an Employee Role's assignment to a Working Pattern on an Effective Date

    Attributes:
        working_pattern_id (Union[Unset, str]):
        effective_from (Union[Unset, datetime.date]): The date when the assignment of the Working Pattern becomes
            effective.
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    working_pattern_id: Union[Unset, str] = UNSET
    effective_from: Union[Unset, datetime.date] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        working_pattern_id = self.working_pattern_id
        effective_from: Union[Unset, str] = UNSET
        if not isinstance(self.effective_from, Unset):
            effective_from = self.effective_from.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if working_pattern_id is not UNSET:
            field_dict["workingPatternId"] = working_pattern_id
        if effective_from is not UNSET:
            field_dict["effectiveFrom"] = effective_from
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        working_pattern_id = d.pop("workingPatternId", UNSET)

        _effective_from = d.pop("effectiveFrom", UNSET)
        effective_from: Union[Unset, datetime.date]
        if isinstance(_effective_from,  Unset):
            effective_from = UNSET
        else:
            effective_from = isoparse(_effective_from).date()




        id = d.pop("id", UNSET)

        employee_role_working_pattern = cls(
            working_pattern_id=working_pattern_id,
            effective_from=effective_from,
            id=id,
        )

        return employee_role_working_pattern

