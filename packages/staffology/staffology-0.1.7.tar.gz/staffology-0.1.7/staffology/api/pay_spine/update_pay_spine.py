from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_pay_spine_request import ContractPaySpineRequest
from ...models.contract_pay_spine_response import ContractPaySpineResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: ContractPaySpineRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{id}".format(
        client.base_url,employerId=employer_id,id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[ContractPaySpineResponse]:
    if response.status_code == 200:
        response_200 = ContractPaySpineResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractPaySpineResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: ContractPaySpineRequest,

) -> Response[ContractPaySpineResponse]:
    """Update PaySpine

     Updates a PaySpine for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (ContractPaySpineRequest):

    Returns:
        Response[ContractPaySpineResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
id=id,
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
    id: str,
    *,
    client: Client,
    json_body: ContractPaySpineRequest,

) -> Optional[ContractPaySpineResponse]:
    """Update PaySpine

     Updates a PaySpine for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (ContractPaySpineRequest):

    Returns:
        Response[ContractPaySpineResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
id=id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: ContractPaySpineRequest,

) -> Response[ContractPaySpineResponse]:
    """Update PaySpine

     Updates a PaySpine for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (ContractPaySpineRequest):

    Returns:
        Response[ContractPaySpineResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
id=id,
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
    id: str,
    *,
    client: Client,
    json_body: ContractPaySpineRequest,

) -> Optional[ContractPaySpineResponse]:
    """Update PaySpine

     Updates a PaySpine for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (ContractPaySpineRequest):

    Returns:
        Response[ContractPaySpineResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
id=id,
client=client,
json_body=json_body,

    )).parsed

