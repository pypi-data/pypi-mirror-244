from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.cost_centre import CostCentre
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    code: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/costcentres/costcentre".format(client.base_url, employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["code"] = code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[CostCentre]:
    if response.status_code == 200:
        response_200 = CostCentre.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[CostCentre]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    code: Union[Unset, None, str] = UNSET,
) -> Response[CostCentre]:
    """Get Cost Centre

     Gets the Cost Centres specified.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):

    Returns:
        Response[CostCentre]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        code=code,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    *,
    client: Client,
    code: Union[Unset, None, str] = UNSET,
) -> Optional[CostCentre]:
    """Get Cost Centre

     Gets the Cost Centres specified.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):

    Returns:
        Response[CostCentre]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        code=code,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    code: Union[Unset, None, str] = UNSET,
) -> Response[CostCentre]:
    """Get Cost Centre

     Gets the Cost Centres specified.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):

    Returns:
        Response[CostCentre]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        code=code,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    code: Union[Unset, None, str] = UNSET,
) -> Optional[CostCentre]:
    """Get Cost Centre

     Gets the Cost Centres specified.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):

    Returns:
        Response[CostCentre]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            code=code,
        )
    ).parsed
