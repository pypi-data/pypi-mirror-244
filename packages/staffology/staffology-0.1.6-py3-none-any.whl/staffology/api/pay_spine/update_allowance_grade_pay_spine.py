from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_allowance_grades_request import ContractAllowanceGradesRequest
from ...models.contract_allowance_grades_response import ContractAllowanceGradesResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    allowance_id: str,
    allowance_grade_id: str,
    *,
    client: Client,
    json_body: ContractAllowanceGradesRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/allowances/{allowanceId}/allowancegrades/{allowanceGradeId}".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id,allowanceId=allowance_id,allowanceGradeId=allowance_grade_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ContractAllowanceGradesResponse]:
    if response.status_code == 200:
        response_200 = ContractAllowanceGradesResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractAllowanceGradesResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    allowance_id: str,
    allowance_grade_id: str,
    *,
    client: Client,
    json_body: ContractAllowanceGradesRequest,

) -> Response[ContractAllowanceGradesResponse]:
    """Update AllowanceGrade

     Update AllowanceGrade for a PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowance_id (str):
        allowance_grade_id (str):
        json_body (ContractAllowanceGradesRequest):

    Returns:
        Response[ContractAllowanceGradesResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowance_id=allowance_id,
allowance_grade_id=allowance_grade_id,
client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    employer_id: str,
    pay_spine_id: str,
    allowance_id: str,
    allowance_grade_id: str,
    *,
    client: Client,
    json_body: ContractAllowanceGradesRequest,

) -> Optional[ContractAllowanceGradesResponse]:
    """Update AllowanceGrade

     Update AllowanceGrade for a PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowance_id (str):
        allowance_grade_id (str):
        json_body (ContractAllowanceGradesRequest):

    Returns:
        Response[ContractAllowanceGradesResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowance_id=allowance_id,
allowance_grade_id=allowance_grade_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    allowance_id: str,
    allowance_grade_id: str,
    *,
    client: Client,
    json_body: ContractAllowanceGradesRequest,

) -> Response[ContractAllowanceGradesResponse]:
    """Update AllowanceGrade

     Update AllowanceGrade for a PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowance_id (str):
        allowance_grade_id (str):
        json_body (ContractAllowanceGradesRequest):

    Returns:
        Response[ContractAllowanceGradesResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowance_id=allowance_id,
allowance_grade_id=allowance_grade_id,
client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    employer_id: str,
    pay_spine_id: str,
    allowance_id: str,
    allowance_grade_id: str,
    *,
    client: Client,
    json_body: ContractAllowanceGradesRequest,

) -> Optional[ContractAllowanceGradesResponse]:
    """Update AllowanceGrade

     Update AllowanceGrade for a PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowance_id (str):
        allowance_grade_id (str):
        json_body (ContractAllowanceGradesRequest):

    Returns:
        Response[ContractAllowanceGradesResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowance_id=allowance_id,
allowance_grade_id=allowance_grade_id,
client=client,
json_body=json_body,

    )).parsed

