from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractJobResultFileResponse")

@attr.s(auto_attribs=True)
class ContractJobResultFileResponse:
    """
    Attributes:
        file_name (Union[Unset, None, str]): Result File name
        uri (Union[Unset, None, str]): Api method URI that can be used to download the result file
    """

    file_name: Union[Unset, None, str] = UNSET
    uri: Union[Unset, None, str] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        file_name = self.file_name
        uri = self.uri

        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if uri is not UNSET:
            field_dict["uri"] = uri

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_name = d.pop("fileName", UNSET)

        uri = d.pop("uri", UNSET)

        contract_job_result_file_response = cls(
            file_name=file_name,
            uri=uri,
        )

        return contract_job_result_file_response

