from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_spinal_point_request import ContractSpinalPointRequest
from ...models.contract_spinal_point_response import ContractSpinalPointResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,
    json_body: ContractSpinalPointRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/spinalpoints/{spinalPointId}".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id,spinalPointId=spinal_point_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[ContractSpinalPointResponse]:
    if response.status_code == 200:
        response_200 = ContractSpinalPointResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractSpinalPointResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,
    json_body: ContractSpinalPointRequest,

) -> Response[ContractSpinalPointResponse]:
    """Update SpinalPoint

     Update SpinalPoint for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):
        json_body (ContractSpinalPointRequest):

    Returns:
        Response[ContractSpinalPointResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
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
    spinal_point_id: str,
    *,
    client: Client,
    json_body: ContractSpinalPointRequest,

) -> Optional[ContractSpinalPointResponse]:
    """Update SpinalPoint

     Update SpinalPoint for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):
        json_body (ContractSpinalPointRequest):

    Returns:
        Response[ContractSpinalPointResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,
    json_body: ContractSpinalPointRequest,

) -> Response[ContractSpinalPointResponse]:
    """Update SpinalPoint

     Update SpinalPoint for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):
        json_body (ContractSpinalPointRequest):

    Returns:
        Response[ContractSpinalPointResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
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
    spinal_point_id: str,
    *,
    client: Client,
    json_body: ContractSpinalPointRequest,

) -> Optional[ContractSpinalPointResponse]:
    """Update SpinalPoint

     Update SpinalPoint for the Employer and PaySpine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):
        json_body (ContractSpinalPointRequest):

    Returns:
        Response[ContractSpinalPointResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,
json_body=json_body,

    )).parsed

