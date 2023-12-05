from typing import Any, Dict, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    accept_invitation: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/invitations/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["acceptInvitation"] = accept_invitation

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    accept_invitation: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Accept Invitation

     Accepts the Invitation.
    The user making this API call must have the email address that the invite was created for and the
    email address must be verified.

    Args:
        id (str):
        accept_invitation (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        accept_invitation=accept_invitation,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    accept_invitation: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Accept Invitation

     Accepts the Invitation.
    The user making this API call must have the email address that the invite was created for and the
    email address must be verified.

    Args:
        id (str):
        accept_invitation (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        accept_invitation=accept_invitation,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
