from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsPriorVersion")

@attr.s(auto_attribs=True)
class FpsPriorVersion:
    """
    Attributes:
        pay_run_entry_id (Union[Unset, str]):
        fps_id (Union[Unset, str]): The Id of the FPS that contains an earlier version of the PayRunEntry
    """

    pay_run_entry_id: Union[Unset, str] = UNSET
    fps_id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        pay_run_entry_id = self.pay_run_entry_id
        fps_id = self.fps_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if pay_run_entry_id is not UNSET:
            field_dict["payRunEntryId"] = pay_run_entry_id
        if fps_id is not UNSET:
            field_dict["fpsId"] = fps_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_run_entry_id = d.pop("payRunEntryId", UNSET)

        fps_id = d.pop("fpsId", UNSET)

        fps_prior_version = cls(
            pay_run_entry_id=pay_run_entry_id,
            fps_id=fps_id,
        )

        return fps_prior_version

