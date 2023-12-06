from typing import Any, Dict

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
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
	    "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }




def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,

) -> Response[Any]:
    """Delete SpinalPoint

     Delete the specified SpinalPoint.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    spinal_point_id: str,
    *,
    client: Client,

) -> Response[Any]:
    """Delete SpinalPoint

     Delete the specified SpinalPoint.

    Args:
        employer_id (str):
        pay_spine_id (str):
        spinal_point_id (str):

    Returns:
        Response[Any]
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


