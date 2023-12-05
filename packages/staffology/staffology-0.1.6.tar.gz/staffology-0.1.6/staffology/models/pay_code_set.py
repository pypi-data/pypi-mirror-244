from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.lgps_pay_category import LgpsPayCategory
from ..models.mcr_pay_category import McrPayCategory
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayCodeSet")

@attr.s(auto_attribs=True)
class PayCodeSet:
    """A PayCodeSet is used to group together a number of PayCodes.

    Attributes:
        name (str): The name of this PayCodeSet
        pay_codes (Union[Unset, None, List[str]]): The Code of any PayCodes included in this PayCodeSet
        use_for_mcr (Union[Unset, bool]):
        mcr_pay_category (Union[Unset, McrPayCategory]):
        use_for_lgps (Union[Unset, bool]): Flag indicating if this PayCodeSet will be used for LGPS pay categorisation
        lgps_pay_category (Union[Unset, LgpsPayCategory]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    pay_codes: Union[Unset, None, List[str]] = UNSET
    use_for_mcr: Union[Unset, bool] = UNSET
    mcr_pay_category: Union[Unset, McrPayCategory] = UNSET
    use_for_lgps: Union[Unset, bool] = UNSET
    lgps_pay_category: Union[Unset, LgpsPayCategory] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        pay_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.pay_codes, Unset):
            if self.pay_codes is None:
                pay_codes = None
            else:
                pay_codes = self.pay_codes




        use_for_mcr = self.use_for_mcr
        mcr_pay_category: Union[Unset, str] = UNSET
        if not isinstance(self.mcr_pay_category, Unset):
            mcr_pay_category = self.mcr_pay_category.value

        use_for_lgps = self.use_for_lgps
        lgps_pay_category: Union[Unset, str] = UNSET
        if not isinstance(self.lgps_pay_category, Unset):
            lgps_pay_category = self.lgps_pay_category.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
            "name": name,
        })
        if pay_codes is not UNSET:
            field_dict["payCodes"] = pay_codes
        if use_for_mcr is not UNSET:
            field_dict["useForMcr"] = use_for_mcr
        if mcr_pay_category is not UNSET:
            field_dict["mcrPayCategory"] = mcr_pay_category
        if use_for_lgps is not UNSET:
            field_dict["useForLgps"] = use_for_lgps
        if lgps_pay_category is not UNSET:
            field_dict["lgpsPayCategory"] = lgps_pay_category
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        pay_codes = cast(List[str], d.pop("payCodes", UNSET))


        use_for_mcr = d.pop("useForMcr", UNSET)

        _mcr_pay_category = d.pop("mcrPayCategory", UNSET)
        mcr_pay_category: Union[Unset, McrPayCategory]
        if isinstance(_mcr_pay_category,  Unset):
            mcr_pay_category = UNSET
        else:
            mcr_pay_category = McrPayCategory(_mcr_pay_category)




        use_for_lgps = d.pop("useForLgps", UNSET)

        _lgps_pay_category = d.pop("lgpsPayCategory", UNSET)
        lgps_pay_category: Union[Unset, LgpsPayCategory]
        if isinstance(_lgps_pay_category,  Unset):
            lgps_pay_category = UNSET
        else:
            lgps_pay_category = LgpsPayCategory(_lgps_pay_category)




        id = d.pop("id", UNSET)

        pay_code_set = cls(
            name=name,
            pay_codes=pay_codes,
            use_for_mcr=use_for_mcr,
            mcr_pay_category=mcr_pay_category,
            use_for_lgps=use_for_lgps,
            lgps_pay_category=lgps_pay_category,
            id=id,
        )

        return pay_code_set

