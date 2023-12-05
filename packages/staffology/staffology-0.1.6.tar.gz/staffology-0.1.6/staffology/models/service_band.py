from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entitlement_band import EntitlementBand
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceBand")

@attr.s(auto_attribs=True)
class ServiceBand:
    """
    Attributes:
        description (Union[Unset, None, str]):
        from_ (Union[Unset, int]):
        to (Union[Unset, int]):
        entitlement_bands (Union[Unset, None, List[EntitlementBand]]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    description: Union[Unset, None, str] = UNSET
    from_: Union[Unset, int] = UNSET
    to: Union[Unset, int] = UNSET
    entitlement_bands: Union[Unset, None, List[EntitlementBand]] = UNSET
    id: Union[Unset, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        from_ = self.from_
        to = self.to
        entitlement_bands: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.entitlement_bands, Unset):
            if self.entitlement_bands is None:
                entitlement_bands = None
            else:
                entitlement_bands = []
                for entitlement_bands_item_data in self.entitlement_bands:
                    entitlement_bands_item = entitlement_bands_item_data.to_dict()

                    entitlement_bands.append(entitlement_bands_item)




        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if entitlement_bands is not UNSET:
            field_dict["entitlementBands"] = entitlement_bands
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        from_ = d.pop("from", UNSET)

        to = d.pop("to", UNSET)

        entitlement_bands = []
        _entitlement_bands = d.pop("entitlementBands", UNSET)
        for entitlement_bands_item_data in (_entitlement_bands or []):
            entitlement_bands_item = EntitlementBand.from_dict(entitlement_bands_item_data)



            entitlement_bands.append(entitlement_bands_item)


        id = d.pop("id", UNSET)

        service_band = cls(
            description=description,
            from_=from_,
            to=to,
            entitlement_bands=entitlement_bands,
            id=id,
        )

        return service_band

