import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SpinalPoint")

@attr.s(auto_attribs=True)
class SpinalPoint:
    """
    Attributes:
        name (str):
        number (int):
        annual_value (float):
        effective_date (datetime.date):
        pay_spine_id (int):
        annual_value_alt_max (Union[Unset, None, float]):
        annual_value_la_inner (Union[Unset, None, float]):
        annual_value_la_inner_alt_max (Union[Unset, None, float]):
        annual_value_la_outer (Union[Unset, None, float]):
        annual_value_la_outer_alt_max (Union[Unset, None, float]):
        annual_value_la_fringe (Union[Unset, None, float]):
        annual_value_la_fringe_alt_max (Union[Unset, None, float]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    number: int
    annual_value: float
    effective_date: datetime.date
    pay_spine_id: int
    annual_value_alt_max: Union[Unset, None, float] = UNSET
    annual_value_la_inner: Union[Unset, None, float] = UNSET
    annual_value_la_inner_alt_max: Union[Unset, None, float] = UNSET
    annual_value_la_outer: Union[Unset, None, float] = UNSET
    annual_value_la_outer_alt_max: Union[Unset, None, float] = UNSET
    annual_value_la_fringe: Union[Unset, None, float] = UNSET
    annual_value_la_fringe_alt_max: Union[Unset, None, float] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        number = self.number
        annual_value = self.annual_value
        effective_date = self.effective_date.isoformat() 
        pay_spine_id = self.pay_spine_id
        annual_value_alt_max = self.annual_value_alt_max
        annual_value_la_inner = self.annual_value_la_inner
        annual_value_la_inner_alt_max = self.annual_value_la_inner_alt_max
        annual_value_la_outer = self.annual_value_la_outer
        annual_value_la_outer_alt_max = self.annual_value_la_outer_alt_max
        annual_value_la_fringe = self.annual_value_la_fringe
        annual_value_la_fringe_alt_max = self.annual_value_la_fringe_alt_max
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
            "number": number,
            "annualValue": annual_value,
            "effectiveDate": effective_date,
            "paySpineId": pay_spine_id,
        })
        if annual_value_alt_max is not UNSET:
            field_dict["annualValueAltMax"] = annual_value_alt_max
        if annual_value_la_inner is not UNSET:
            field_dict["annualValueLAInner"] = annual_value_la_inner
        if annual_value_la_inner_alt_max is not UNSET:
            field_dict["annualValueLAInnerAltMax"] = annual_value_la_inner_alt_max
        if annual_value_la_outer is not UNSET:
            field_dict["annualValueLAOuter"] = annual_value_la_outer
        if annual_value_la_outer_alt_max is not UNSET:
            field_dict["annualValueLAOuterAltMax"] = annual_value_la_outer_alt_max
        if annual_value_la_fringe is not UNSET:
            field_dict["annualValueLAFringe"] = annual_value_la_fringe
        if annual_value_la_fringe_alt_max is not UNSET:
            field_dict["annualValueLAFringeAltMax"] = annual_value_la_fringe_alt_max
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        number = d.pop("number")

        annual_value = d.pop("annualValue")

        effective_date = isoparse(d.pop("effectiveDate")).date()




        pay_spine_id = d.pop("paySpineId")

        annual_value_alt_max = d.pop("annualValueAltMax", UNSET)

        annual_value_la_inner = d.pop("annualValueLAInner", UNSET)

        annual_value_la_inner_alt_max = d.pop("annualValueLAInnerAltMax", UNSET)

        annual_value_la_outer = d.pop("annualValueLAOuter", UNSET)

        annual_value_la_outer_alt_max = d.pop("annualValueLAOuterAltMax", UNSET)

        annual_value_la_fringe = d.pop("annualValueLAFringe", UNSET)

        annual_value_la_fringe_alt_max = d.pop("annualValueLAFringeAltMax", UNSET)

        id = d.pop("id", UNSET)

        spinal_point = cls(
            name=name,
            number=number,
            annual_value=annual_value,
            effective_date=effective_date,
            pay_spine_id=pay_spine_id,
            annual_value_alt_max=annual_value_alt_max,
            annual_value_la_inner=annual_value_la_inner,
            annual_value_la_inner_alt_max=annual_value_la_inner_alt_max,
            annual_value_la_outer=annual_value_la_outer,
            annual_value_la_outer_alt_max=annual_value_la_outer_alt_max,
            annual_value_la_fringe=annual_value_la_fringe,
            annual_value_la_fringe_alt_max=annual_value_la_fringe_alt_max,
            id=id,
        )

        return spinal_point

