from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.tenant import Tenant
from ...models.update_fav_icon_tenant_multipart_data import UpdateFavIconTenantMultipartData
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    multipart_data: UpdateFavIconTenantMultipartData,

) -> Dict[str, Any]:
    url = "{}/tenants/{id}/favicon".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    multipart_multipart_data = multipart_data.to_multipart()




    return {
	    "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Tenant]:
    if response.status_code == 200:
        response_200 = Tenant.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Tenant]:
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
    multipart_data: UpdateFavIconTenantMultipartData,

) -> Response[Tenant]:
    """Upload Favicon

     Upload an image to use as favicon. We'll upload it and set the URL on the FavIcon property of the
    Tenant.

    Args:
        id (str):
        multipart_data (UpdateFavIconTenantMultipartData):

    Returns:
        Response[Tenant]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
multipart_data=multipart_data,

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
    multipart_data: UpdateFavIconTenantMultipartData,

) -> Optional[Tenant]:
    """Upload Favicon

     Upload an image to use as favicon. We'll upload it and set the URL on the FavIcon property of the
    Tenant.

    Args:
        id (str):
        multipart_data (UpdateFavIconTenantMultipartData):

    Returns:
        Response[Tenant]
    """


    return sync_detailed(
        id=id,
client=client,
multipart_data=multipart_data,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    multipart_data: UpdateFavIconTenantMultipartData,

) -> Response[Tenant]:
    """Upload Favicon

     Upload an image to use as favicon. We'll upload it and set the URL on the FavIcon property of the
    Tenant.

    Args:
        id (str):
        multipart_data (UpdateFavIconTenantMultipartData):

    Returns:
        Response[Tenant]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
multipart_data=multipart_data,

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
    multipart_data: UpdateFavIconTenantMultipartData,

) -> Optional[Tenant]:
    """Upload Favicon

     Upload an image to use as favicon. We'll upload it and set the URL on the FavIcon property of the
    Tenant.

    Args:
        id (str):
        multipart_data (UpdateFavIconTenantMultipartData):

    Returns:
        Response[Tenant]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
multipart_data=multipart_data,

    )).parsed

