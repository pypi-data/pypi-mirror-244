from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.employer_group import EmployerGroup
from ...types import Response


def _get_kwargs(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Dict[str, Any]:
    url = "{}/employers/groups/{code}".format(client.base_url, code=code)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, EmployerGroup]]:
    if response.status_code == 200:
        response_200 = EmployerGroup.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, EmployerGroup]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Response[Union[Any, EmployerGroup]]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[Union[Any, EmployerGroup]]
    """

    kwargs = _get_kwargs(
        code=code,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Optional[Union[Any, EmployerGroup]]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[Union[Any, EmployerGroup]]
    """

    return sync_detailed(
        code=code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Response[Union[Any, EmployerGroup]]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[Union[Any, EmployerGroup]]
    """

    kwargs = _get_kwargs(
        code=code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Optional[Union[Any, EmployerGroup]]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[Union[Any, EmployerGroup]]
    """

    return (
        await asyncio_detailed(
            code=code,
            client=client,
            json_body=json_body,
        )
    ).parsed
