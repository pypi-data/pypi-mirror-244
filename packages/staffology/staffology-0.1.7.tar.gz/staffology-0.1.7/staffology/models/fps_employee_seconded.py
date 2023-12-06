from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeSeconded")

@attr.s(auto_attribs=True)
class FpsEmployeeSeconded:
    """
    Attributes:
        in_out_uk (Union[Unset, None, str]):
        stay_183_days_or_more (Union[Unset, None, str]):
        stay_less_than_183_days (Union[Unset, None, str]):
        eea_citizen (Union[Unset, None, str]):
        ep_m6 (Union[Unset, None, str]):
    """

    in_out_uk: Union[Unset, None, str] = UNSET
    stay_183_days_or_more: Union[Unset, None, str] = UNSET
    stay_less_than_183_days: Union[Unset, None, str] = UNSET
    eea_citizen: Union[Unset, None, str] = UNSET
    ep_m6: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        in_out_uk = self.in_out_uk
        stay_183_days_or_more = self.stay_183_days_or_more
        stay_less_than_183_days = self.stay_less_than_183_days
        eea_citizen = self.eea_citizen
        ep_m6 = self.ep_m6

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if in_out_uk is not UNSET:
            field_dict["inOutUK"] = in_out_uk
        if stay_183_days_or_more is not UNSET:
            field_dict["stay183DaysOrMore"] = stay_183_days_or_more
        if stay_less_than_183_days is not UNSET:
            field_dict["stayLessThan183Days"] = stay_less_than_183_days
        if eea_citizen is not UNSET:
            field_dict["eeaCitizen"] = eea_citizen
        if ep_m6 is not UNSET:
            field_dict["epM6"] = ep_m6

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        in_out_uk = d.pop("inOutUK", UNSET)

        stay_183_days_or_more = d.pop("stay183DaysOrMore", UNSET)

        stay_less_than_183_days = d.pop("stayLessThan183Days", UNSET)

        eea_citizen = d.pop("eeaCitizen", UNSET)

        ep_m6 = d.pop("epM6", UNSET)

        fps_employee_seconded = cls(
            in_out_uk=in_out_uk,
            stay_183_days_or_more=stay_183_days_or_more,
            stay_less_than_183_days=stay_less_than_183_days,
            eea_citizen=eea_citizen,
            ep_m6=ep_m6,
        )

        return fps_employee_seconded

