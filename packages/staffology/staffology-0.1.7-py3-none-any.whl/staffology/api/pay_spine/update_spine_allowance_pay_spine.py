from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_spine_allowance_request import ContractSpineAllowanceRequest
from ...models.contract_spine_allowance_response import ContractSpineAllowanceResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    allowanceid: str,
    *,
    client: Client,
    json_body: ContractSpineAllowanceRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/allowances/{allowanceid}".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id,allowanceid=allowanceid)

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


def _parse_response(*, response: httpx.Response) -> Optional[ContractSpineAllowanceResponse]:
    if response.status_code == 200:
        response_200 = ContractSpineAllowanceResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractSpineAllowanceResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    allowanceid: str,
    *,
    client: Client,
    json_body: ContractSpineAllowanceRequest,

) -> Response[ContractSpineAllowanceResponse]:
    """Update SpineAllowance

     Update Allowance for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowanceid (str):
        json_body (ContractSpineAllowanceRequest):

    Returns:
        Response[ContractSpineAllowanceResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowanceid=allowanceid,
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
    allowanceid: str,
    *,
    client: Client,
    json_body: ContractSpineAllowanceRequest,

) -> Optional[ContractSpineAllowanceResponse]:
    """Update SpineAllowance

     Update Allowance for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowanceid (str):
        json_body (ContractSpineAllowanceRequest):

    Returns:
        Response[ContractSpineAllowanceResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowanceid=allowanceid,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    allowanceid: str,
    *,
    client: Client,
    json_body: ContractSpineAllowanceRequest,

) -> Response[ContractSpineAllowanceResponse]:
    """Update SpineAllowance

     Update Allowance for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowanceid (str):
        json_body (ContractSpineAllowanceRequest):

    Returns:
        Response[ContractSpineAllowanceResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowanceid=allowanceid,
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
    allowanceid: str,
    *,
    client: Client,
    json_body: ContractSpineAllowanceRequest,

) -> Optional[ContractSpineAllowanceResponse]:
    """Update SpineAllowance

     Update Allowance for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):
        allowanceid (str):
        json_body (ContractSpineAllowanceRequest):

    Returns:
        Response[ContractSpineAllowanceResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
allowanceid=allowanceid,
client=client,
json_body=json_body,

    )).parsed

