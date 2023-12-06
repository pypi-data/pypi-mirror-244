from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_spinal_point_response import ContractSpinalPointResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/spinalpoints/{spinalPointId}".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id,spinalPointId=spinal_point_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractSpinalPointResponse]]:
    if response.status_code == 200:
        response_200 = ContractSpinalPointResponse.from_dict(response.json())



        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractSpinalPointResponse]]:
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

) -> Response[Union[Any, ContractSpinalPointResponse]]:
    """Get SpinalPoint

     Get SpinalPoint for an Employer and Payspine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Union[Any, ContractSpinalPointResponse]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,

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

) -> Optional[Union[Any, ContractSpinalPointResponse]]:
    """Get SpinalPoint

     Get SpinalPoint for an Employer and Payspine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Union[Any, ContractSpinalPointResponse]]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,

) -> Response[Union[Any, ContractSpinalPointResponse]]:
    """Get SpinalPoint

     Get SpinalPoint for an Employer and Payspine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Union[Any, ContractSpinalPointResponse]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,

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

) -> Optional[Union[Any, ContractSpinalPointResponse]]:
    """Get SpinalPoint

     Get SpinalPoint for an Employer and Payspine.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Union[Any, ContractSpinalPointResponse]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
spinal_point_id=spinal_point_id,
client=client,

    )).parsed

