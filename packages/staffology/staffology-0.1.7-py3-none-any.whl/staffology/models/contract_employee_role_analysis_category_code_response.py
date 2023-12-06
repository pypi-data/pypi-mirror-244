from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractEmployeeRoleAnalysisCategoryCodeResponse")

@attr.s(auto_attribs=True)
class ContractEmployeeRoleAnalysisCategoryCodeResponse:
    """
    Attributes:
        id (Union[Unset, str]): Employee Role Analysis Category Code identifier
        code (Union[Unset, None, str]): Analysis Category code
        color (Union[Unset, None, str]): Analysis Category code color
        title (Union[Unset, None, str]): Analysis Category code Title
        weighting (Union[Unset, float]): Weightage for analysis category code
        analysis_category_name (Union[Unset, None, str]): Analysis category name for AnalysisCategory code
        analysis_category_public_id (Union[Unset, str]): Analysis category identifier
        is_primary (Union[Unset, bool]): Return whether Employee Role is primary for not
    """

    id: Union[Unset, str] = UNSET
    code: Union[Unset, None, str] = UNSET
    color: Union[Unset, None, str] = UNSET
    title: Union[Unset, None, str] = UNSET
    weighting: Union[Unset, float] = UNSET
    analysis_category_name: Union[Unset, None, str] = UNSET
    analysis_category_public_id: Union[Unset, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        code = self.code
        color = self.color
        title = self.title
        weighting = self.weighting
        analysis_category_name = self.analysis_category_name
        analysis_category_public_id = self.analysis_category_public_id
        is_primary = self.is_primary

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if code is not UNSET:
            field_dict["code"] = code
        if color is not UNSET:
            field_dict["color"] = color
        if title is not UNSET:
            field_dict["title"] = title
        if weighting is not UNSET:
            field_dict["weighting"] = weighting
        if analysis_category_name is not UNSET:
            field_dict["analysisCategoryName"] = analysis_category_name
        if analysis_category_public_id is not UNSET:
            field_dict["analysisCategoryPublicId"] = analysis_category_public_id
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        code = d.pop("code", UNSET)

        color = d.pop("color", UNSET)

        title = d.pop("title", UNSET)

        weighting = d.pop("weighting", UNSET)

        analysis_category_name = d.pop("analysisCategoryName", UNSET)

        analysis_category_public_id = d.pop("analysisCategoryPublicId", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        contract_employee_role_analysis_category_code_response = cls(
            id=id,
            code=code,
            color=color,
            title=title,
            weighting=weighting,
            analysis_category_name=analysis_category_name,
            analysis_category_public_id=analysis_category_public_id,
            is_primary=is_primary,
        )

        return contract_employee_role_analysis_category_code_response

