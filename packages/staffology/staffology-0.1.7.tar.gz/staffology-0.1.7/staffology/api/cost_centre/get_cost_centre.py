from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.cost_centre import CostCentre
from ...types import Response


def _get_kwargs(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/costcentres/{code}".format(client.base_url, employerId=employer_id, code=code)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    code: str,
    *,
    client: Client,
) -> Response[CostCentre]:
    """Get Cost Centre (deprecated)

     Gets the Cost Centres specified.
    Use the other GET endpoint that supports non-alphanumeric characters for a cost centre code

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[CostCentre]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Optional[CostCentre]:
    """Get Cost Centre (deprecated)

     Gets the Cost Centres specified.
    Use the other GET endpoint that supports non-alphanumeric characters for a cost centre code

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[CostCentre]
    """

    return sync_detailed(
        employer_id=employer_id,
        code=code,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Response[CostCentre]:
    """Get Cost Centre (deprecated)

     Gets the Cost Centres specified.
    Use the other GET endpoint that supports non-alphanumeric characters for a cost centre code

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[CostCentre]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Optional[CostCentre]:
    """Get Cost Centre (deprecated)

     Gets the Cost Centres specified.
    Use the other GET endpoint that supports non-alphanumeric characters for a cost centre code

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[CostCentre]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            code=code,
            client=client,
        )
    ).parsed
