from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pricing_table import PricingTable
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: PricingTable,

) -> Dict[str, Any]:
    url = "{}/tenants/{id}/pricingtables".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PricingTable]]:
    if response.status_code == 201:
        response_201 = PricingTable.from_dict(response.json())



        return response_201
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PricingTable]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: PricingTable,

) -> Response[Union[Any, PricingTable]]:
    """Create PricingTable

     Create a PricingTable

    Args:
        id (str):
        json_body (PricingTable):

    Returns:
        Response[Union[Any, PricingTable]]
    """


    kwargs = _get_kwargs(
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
    id: str,
    *,
    client: Client,
    json_body: PricingTable,

) -> Optional[Union[Any, PricingTable]]:
    """Create PricingTable

     Create a PricingTable

    Args:
        id (str):
        json_body (PricingTable):

    Returns:
        Response[Union[Any, PricingTable]]
    """


    return sync_detailed(
        id=id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: PricingTable,

) -> Response[Union[Any, PricingTable]]:
    """Create PricingTable

     Create a PricingTable

    Args:
        id (str):
        json_body (PricingTable):

    Returns:
        Response[Union[Any, PricingTable]]
    """


    kwargs = _get_kwargs(
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
    id: str,
    *,
    client: Client,
    json_body: PricingTable,

) -> Optional[Union[Any, PricingTable]]:
    """Create PricingTable

     Create a PricingTable

    Args:
        id (str):
        json_body (PricingTable):

    Returns:
        Response[Union[Any, PricingTable]]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
json_body=json_body,

    )).parsed

