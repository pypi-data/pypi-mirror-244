import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.contract_job_result_response import ContractJobResultResponse
from ..models.job_status import JobStatus
from ..models.job_type import JobType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContractJobResponse")

@attr.s(auto_attribs=True)
class ContractJobResponse:
    """
    Attributes:
        id (Union[Unset, str]): Job public Id.
        employer_id (Union[Unset, str]): Employer public Id.
        type (Union[Unset, JobType]):
        sub_type (Union[Unset, None, str]): The Job request payload.
        name (Union[Unset, None, str]): The Job name in UI, e.g. uploaded file for Import, or report display name for
            Report
        output_format (Union[Unset, None, str]): The Job output format, e.g. json/csv/pdf for Report, or something else
            for other Job types.
        status (Union[Unset, JobStatus]):
        expiry_date (Union[Unset, None, datetime.date]): Results expiry date where applicable.
        result (Union[Unset, ContractJobResultResponse]):
        created_date (Union[Unset, datetime.date]): Job Created date.
        updated_date (Union[Unset, None, datetime.date]): Job Updated date where applicable.
    """

    id: Union[Unset, str] = UNSET
    employer_id: Union[Unset, str] = UNSET
    type: Union[Unset, JobType] = UNSET
    sub_type: Union[Unset, None, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    output_format: Union[Unset, None, str] = UNSET
    status: Union[Unset, JobStatus] = UNSET
    expiry_date: Union[Unset, None, datetime.date] = UNSET
    result: Union[Unset, ContractJobResultResponse] = UNSET
    created_date: Union[Unset, datetime.date] = UNSET
    updated_date: Union[Unset, None, datetime.date] = UNSET


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        employer_id = self.employer_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        sub_type = self.sub_type
        name = self.name
        output_format = self.output_format
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        expiry_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.expiry_date, Unset):
            expiry_date = self.expiry_date.isoformat() if self.expiry_date else None

        result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        updated_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.updated_date, Unset):
            updated_date = self.updated_date.isoformat() if self.updated_date else None


        field_dict: Dict[str, Any] = {}
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if employer_id is not UNSET:
            field_dict["employerId"] = employer_id
        if type is not UNSET:
            field_dict["type"] = type
        if sub_type is not UNSET:
            field_dict["subType"] = sub_type
        if name is not UNSET:
            field_dict["name"] = name
        if output_format is not UNSET:
            field_dict["outputFormat"] = output_format
        if status is not UNSET:
            field_dict["status"] = status
        if expiry_date is not UNSET:
            field_dict["expiryDate"] = expiry_date
        if result is not UNSET:
            field_dict["result"] = result
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if updated_date is not UNSET:
            field_dict["updatedDate"] = updated_date

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        employer_id = d.pop("employerId", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, JobType]
        if isinstance(_type,  Unset):
            type = UNSET
        else:
            type = JobType(_type)




        sub_type = d.pop("subType", UNSET)

        name = d.pop("name", UNSET)

        output_format = d.pop("outputFormat", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = JobStatus(_status)




        _expiry_date = d.pop("expiryDate", UNSET)
        expiry_date: Union[Unset, None, datetime.date]
        if _expiry_date is None:
            expiry_date = None
        elif isinstance(_expiry_date,  Unset):
            expiry_date = UNSET
        else:
            expiry_date = isoparse(_expiry_date).date()




        _result = d.pop("result", UNSET)
        result: Union[Unset, ContractJobResultResponse]
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = ContractJobResultResponse.from_dict(_result)




        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.date]
        if isinstance(_created_date,  Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date).date()




        _updated_date = d.pop("updatedDate", UNSET)
        updated_date: Union[Unset, None, datetime.date]
        if _updated_date is None:
            updated_date = None
        elif isinstance(_updated_date,  Unset):
            updated_date = UNSET
        else:
            updated_date = isoparse(_updated_date).date()




        contract_job_response = cls(
            id=id,
            employer_id=employer_id,
            type=type,
            sub_type=sub_type,
            name=name,
            output_format=output_format,
            status=status,
            expiry_date=expiry_date,
            result=result,
            created_date=created_date,
            updated_date=updated_date,
        )

        return contract_job_response

