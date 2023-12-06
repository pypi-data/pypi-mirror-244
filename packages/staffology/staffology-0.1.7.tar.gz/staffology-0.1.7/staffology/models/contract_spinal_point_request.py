import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractSpinalPointRequest")

@attr.s(auto_attribs=True)
class ContractSpinalPointRequest:
    """
    Attributes:
        name (Union[Unset, None, str]): Name of the Spinal Point
        number (Union[Unset, int]): Number of Spinal Point within the Scale
        annual_value (Union[Unset, float]): Annual Value for the Spinal Point
        annual_value_alt_max (Union[Unset, float]): Annual Value for the Spinal Point (Alternative Max Value)
        annual_value_la_inner (Union[Unset, float]): Annual Value for the Spinal Point Inner London Allowance
        annual_value_la_inner_alt_max (Union[Unset, float]): Annual Value for the Spinal Point Inner LA (Alt Max Value)
        annual_value_la_outer (Union[Unset, float]): Annual Value for the Spinal Point Outer London Allowance
        annual_value_la_outer_alt_max (Union[Unset, float]): Annual Value for the Spinal Point Outer LA (Alt Max Value)
        annual_value_la_fringe (Union[Unset, float]): Annual Value for the Spinal Point Fringe London Allowance
        annual_value_la_fringe_alt_max (Union[Unset, float]): Annual Value for the Spinal Point Fringe LA (Alt Max
            Value)
        effective_date (Union[Unset, datetime.date]): Date these rates became effective
    """

    name: Union[Unset, None, str] = UNSET
    number: Union[Unset, int] = UNSET
    annual_value: Union[Unset, float] = UNSET
    annual_value_alt_max: Union[Unset, float] = UNSET
    annual_value_la_inner: Union[Unset, float] = UNSET
    annual_value_la_inner_alt_max: Union[Unset, float] = UNSET
    annual_value_la_outer: Union[Unset, float] = UNSET
    annual_value_la_outer_alt_max: Union[Unset, float] = UNSET
    annual_value_la_fringe: Union[Unset, float] = UNSET
    annual_value_la_fringe_alt_max: Union[Unset, float] = UNSET
    effective_date: Union[Unset, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        number = self.number
        annual_value = self.annual_value
        annual_value_alt_max = self.annual_value_alt_max
        annual_value_la_inner = self.annual_value_la_inner
        annual_value_la_inner_alt_max = self.annual_value_la_inner_alt_max
        annual_value_la_outer = self.annual_value_la_outer
        annual_value_la_outer_alt_max = self.annual_value_la_outer_alt_max
        annual_value_la_fringe = self.annual_value_la_fringe
        annual_value_la_fringe_alt_max = self.annual_value_la_fringe_alt_max
        effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if number is not UNSET:
            field_dict["number"] = number
        if annual_value is not UNSET:
            field_dict["annualValue"] = annual_value
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
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        number = d.pop("number", UNSET)

        annual_value = d.pop("annualValue", UNSET)

        annual_value_alt_max = d.pop("annualValueAltMax", UNSET)

        annual_value_la_inner = d.pop("annualValueLAInner", UNSET)

        annual_value_la_inner_alt_max = d.pop("annualValueLAInnerAltMax", UNSET)

        annual_value_la_outer = d.pop("annualValueLAOuter", UNSET)

        annual_value_la_outer_alt_max = d.pop("annualValueLAOuterAltMax", UNSET)

        annual_value_la_fringe = d.pop("annualValueLAFringe", UNSET)

        annual_value_la_fringe_alt_max = d.pop("annualValueLAFringeAltMax", UNSET)

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: Union[Unset, datetime.date]
        if isinstance(_effective_date,  Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date).date()




        contract_spinal_point_request = cls(
            name=name,
            number=number,
            annual_value=annual_value,
            annual_value_alt_max=annual_value_alt_max,
            annual_value_la_inner=annual_value_la_inner,
            annual_value_la_inner_alt_max=annual_value_la_inner_alt_max,
            annual_value_la_outer=annual_value_la_outer,
            annual_value_la_outer_alt_max=annual_value_la_outer_alt_max,
            annual_value_la_fringe=annual_value_la_fringe,
            annual_value_la_fringe_alt_max=annual_value_la_fringe_alt_max,
            effective_date=effective_date,
        )

        return contract_spinal_point_request

