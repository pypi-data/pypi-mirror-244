from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractPaylineAnalysisCategoriesCodes")

@attr.s(auto_attribs=True)
class ContractPaylineAnalysisCategoriesCodes:
    """
    Attributes:
        analysis_category (Union[Unset, None, str]): AnalysisCategory Model
        analysis_category_code (Union[Unset, None, str]): AnalysisCategoryCode Model
        analysis_category_id (Union[Unset, None, str]): AnalysisCategory Identifier
        analysis_category_code_id (Union[Unset, None, str]): AnalysisCategoryCode Identifier
    """

    analysis_category: Union[Unset, None, str] = UNSET
    analysis_category_code: Union[Unset, None, str] = UNSET
    analysis_category_id: Union[Unset, None, str] = UNSET
    analysis_category_code_id: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        analysis_category = self.analysis_category
        analysis_category_code = self.analysis_category_code
        analysis_category_id = self.analysis_category_id
        analysis_category_code_id = self.analysis_category_code_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if analysis_category is not UNSET:
            field_dict["analysisCategory"] = analysis_category
        if analysis_category_code is not UNSET:
            field_dict["analysisCategoryCode"] = analysis_category_code
        if analysis_category_id is not UNSET:
            field_dict["analysisCategoryId"] = analysis_category_id
        if analysis_category_code_id is not UNSET:
            field_dict["analysisCategoryCodeId"] = analysis_category_code_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        analysis_category = d.pop("analysisCategory", UNSET)

        analysis_category_code = d.pop("analysisCategoryCode", UNSET)

        analysis_category_id = d.pop("analysisCategoryId", UNSET)

        analysis_category_code_id = d.pop("analysisCategoryCodeId", UNSET)

        contract_payline_analysis_categories_codes = cls(
            analysis_category=analysis_category,
            analysis_category_code=analysis_category_code,
            analysis_category_id=analysis_category_id,
            analysis_category_code_id=analysis_category_code_id,
        )

        return contract_payline_analysis_categories_codes

