from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractAnalysisCategoryCodeRequest")

@attr.s(auto_attribs=True)
class ContractAnalysisCategoryCodeRequest:
    """
    Attributes:
        code (Union[Unset, None, str]):
        title (Union[Unset, None, str]):
        color (Union[Unset, None, str]):
        accounting_code (Union[Unset, None, str]):
    """

    code: Union[Unset, None, str] = UNSET
    title: Union[Unset, None, str] = UNSET
    color: Union[Unset, None, str] = UNSET
    accounting_code: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        title = self.title
        color = self.color
        accounting_code = self.accounting_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if code is not UNSET:
            field_dict["code"] = code
        if title is not UNSET:
            field_dict["title"] = title
        if color is not UNSET:
            field_dict["color"] = color
        if accounting_code is not UNSET:
            field_dict["accountingCode"] = accounting_code

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        title = d.pop("title", UNSET)

        color = d.pop("color", UNSET)

        accounting_code = d.pop("accountingCode", UNSET)

        contract_analysis_category_code_request = cls(
            code=code,
            title=title,
            color=color,
            accounting_code=accounting_code,
        )

        return contract_analysis_category_code_request

