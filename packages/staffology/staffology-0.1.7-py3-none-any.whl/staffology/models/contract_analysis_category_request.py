from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractAnalysisCategoryRequest")

@attr.s(auto_attribs=True)
class ContractAnalysisCategoryRequest:
    """
    Attributes:
        name (Union[Unset, None, str]): Analysis Category Name
    """

    name: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        contract_analysis_category_request = cls(
            name=name,
        )

        return contract_analysis_category_request

