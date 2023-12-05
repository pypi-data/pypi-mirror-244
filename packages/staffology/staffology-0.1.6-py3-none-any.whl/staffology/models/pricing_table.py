from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pricing_band import PricingBand
from ..types import UNSET, Unset

T = TypeVar("T", bound="PricingTable")

@attr.s(auto_attribs=True)
class PricingTable:
    """
    Attributes:
        name (Union[Unset, None, str]):
        minimum_charge (Union[Unset, float]):
        bands (Union[Unset, None, List[PricingBand]]):
        is_default (Union[Unset, bool]):
        net_suite_item_code (Union[Unset, None, str]):
        net_suite_description (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: Union[Unset, None, str] = UNSET
    minimum_charge: Union[Unset, float] = UNSET
    bands: Union[Unset, None, List[PricingBand]] = UNSET
    is_default: Union[Unset, bool] = UNSET
    net_suite_item_code: Union[Unset, None, str] = UNSET
    net_suite_description: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        minimum_charge = self.minimum_charge
        bands: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.bands, Unset):
            if self.bands is None:
                bands = None
            else:
                bands = []
                for bands_item_data in self.bands:
                    bands_item = bands_item_data.to_dict()

                    bands.append(bands_item)




        is_default = self.is_default
        net_suite_item_code = self.net_suite_item_code
        net_suite_description = self.net_suite_description
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if minimum_charge is not UNSET:
            field_dict["minimumCharge"] = minimum_charge
        if bands is not UNSET:
            field_dict["bands"] = bands
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default
        if net_suite_item_code is not UNSET:
            field_dict["netSuiteItemCode"] = net_suite_item_code
        if net_suite_description is not UNSET:
            field_dict["netSuiteDescription"] = net_suite_description
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        minimum_charge = d.pop("minimumCharge", UNSET)

        bands = []
        _bands = d.pop("bands", UNSET)
        for bands_item_data in (_bands or []):
            bands_item = PricingBand.from_dict(bands_item_data)



            bands.append(bands_item)


        is_default = d.pop("isDefault", UNSET)

        net_suite_item_code = d.pop("netSuiteItemCode", UNSET)

        net_suite_description = d.pop("netSuiteDescription", UNSET)

        id = d.pop("id", UNSET)

        pricing_table = cls(
            name=name,
            minimum_charge=minimum_charge,
            bands=bands,
            is_default=is_default,
            net_suite_item_code=net_suite_item_code,
            net_suite_description=net_suite_description,
            id=id,
        )

        return pricing_table

