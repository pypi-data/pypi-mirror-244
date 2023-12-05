from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.employer import Employer
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Employer]:
    if response.status_code == 200:
        response_200 = Employer.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Employer]:
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
) -> Response[Employer]:
    """Get an Employer

    Args:
        id (str):

    Returns:
        Response[Employer]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
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
) -> Optional[Employer]:
    """Get an Employer

    Args:
        id (str):

    Returns:
        Response[Employer]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Employer]:
    """Get an Employer

    Args:
        id (str):

    Returns:
        Response[Employer]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
) -> Optional[Employer]:
    """Get an Employer

    Args:
        id (str):

    Returns:
        Response[Employer]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
