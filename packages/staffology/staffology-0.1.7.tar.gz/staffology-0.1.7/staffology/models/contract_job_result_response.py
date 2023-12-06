from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.contract_job_result_file_response import ContractJobResultFileResponse
from ..models.contract_job_result_response_metadata import ContractJobResultResponseMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractJobResultResponse")

@attr.s(auto_attribs=True)
class ContractJobResultResponse:
    """
    Attributes:
        file (Union[Unset, ContractJobResultFileResponse]):
        metadata (Union[Unset, None, ContractJobResultResponseMetadata]): Job result metadata, e.g. Employee Import
            stats
        errors (Union[Unset, None, List[str]]): Job execution's errors.
    """

    file: Union[Unset, ContractJobResultFileResponse] = UNSET
    metadata: Union[Unset, None, ContractJobResultResponseMetadata] = UNSET
    errors: Union[Unset, None, List[str]] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        file: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict()

        metadata: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict() if self.metadata else None

        errors: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.errors, Unset):
            if self.errors is None:
                errors = None
            else:
                errors = self.errors





        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if file is not UNSET:
            field_dict["file"] = file
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _file = d.pop("file", UNSET)
        file: Union[Unset, ContractJobResultFileResponse]
        if isinstance(_file,  Unset):
            file = UNSET
        else:
            file = ContractJobResultFileResponse.from_dict(_file)




        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, None, ContractJobResultResponseMetadata]
        if _metadata is None:
            metadata = None
        elif isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ContractJobResultResponseMetadata.from_dict(_metadata)




        errors = cast(List[str], d.pop("errors", UNSET))


        contract_job_result_response = cls(
            file=file,
            metadata=metadata,
            errors=errors,
        )

        return contract_job_result_response

