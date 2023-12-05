from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.evc_settings import EvcSettings
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: EvcSettings,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/evcsettings".format(client.base_url, employerId=employer_id, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[EvcSettings]:
    if response.status_code == 200:
        response_200 = EvcSettings.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[EvcSettings]:
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
    json_body: EvcSettings,
) -> Response[EvcSettings]:
    """Update EvcSettings

    Args:
        employer_id (str):
        id (str):
        json_body (EvcSettings): Employee Settings related to the Employee Verification Programme

    Returns:
        Response[EvcSettings]
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
    json_body: EvcSettings,
) -> Optional[EvcSettings]:
    """Update EvcSettings

    Args:
        employer_id (str):
        id (str):
        json_body (EvcSettings): Employee Settings related to the Employee Verification Programme

    Returns:
        Response[EvcSettings]
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
    json_body: EvcSettings,
) -> Response[EvcSettings]:
    """Update EvcSettings

    Args:
        employer_id (str):
        id (str):
        json_body (EvcSettings): Employee Settings related to the Employee Verification Programme

    Returns:
        Response[EvcSettings]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: EvcSettings,
) -> Optional[EvcSettings]:
    """Update EvcSettings

    Args:
        employer_id (str):
        id (str):
        json_body (EvcSettings): Employee Settings related to the Employee Verification Programme

    Returns:
        Response[EvcSettings]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
