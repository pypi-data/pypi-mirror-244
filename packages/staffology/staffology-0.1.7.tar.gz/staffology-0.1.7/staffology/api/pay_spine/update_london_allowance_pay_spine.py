from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_london_allowance_request import ContractLondonAllowanceRequest
from ...models.contract_london_allowance_response import ContractLondonAllowanceResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    london_allowance_id: str,
    *,
    client: Client,
    json_body: ContractLondonAllowanceRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/londonallowances/{londonAllowanceId}".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id,londonAllowanceId=london_allowance_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[ContractLondonAllowanceResponse]:
    if response.status_code == 200:
        response_200 = ContractLondonAllowanceResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractLondonAllowanceResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    london_allowance_id: str,
    *,
    client: Client,
    json_body: ContractLondonAllowanceRequest,

) -> Response[ContractLondonAllowanceResponse]:
    """Update LondonAllowance

     Update LondonAllowance for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        london_allowance_id (str):
        json_body (ContractLondonAllowanceRequest):

    Returns:
        Response[ContractLondonAllowanceResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
london_allowance_id=london_allowance_id,
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
    london_allowance_id: str,
    *,
    client: Client,
    json_body: ContractLondonAllowanceRequest,

) -> Optional[ContractLondonAllowanceResponse]:
    """Update LondonAllowance

     Update LondonAllowance for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        london_allowance_id (str):
        json_body (ContractLondonAllowanceRequest):

    Returns:
        Response[ContractLondonAllowanceResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
london_allowance_id=london_allowance_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    london_allowance_id: str,
    *,
    client: Client,
    json_body: ContractLondonAllowanceRequest,

) -> Response[ContractLondonAllowanceResponse]:
    """Update LondonAllowance

     Update LondonAllowance for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        london_allowance_id (str):
        json_body (ContractLondonAllowanceRequest):

    Returns:
        Response[ContractLondonAllowanceResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
london_allowance_id=london_allowance_id,
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
    london_allowance_id: str,
    *,
    client: Client,
    json_body: ContractLondonAllowanceRequest,

) -> Optional[ContractLondonAllowanceResponse]:
    """Update LondonAllowance

     Update LondonAllowance for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        london_allowance_id (str):
        json_body (ContractLondonAllowanceRequest):

    Returns:
        Response[ContractLondonAllowanceResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
london_allowance_id=london_allowance_id,
client=client,
json_body=json_body,

    )).parsed

