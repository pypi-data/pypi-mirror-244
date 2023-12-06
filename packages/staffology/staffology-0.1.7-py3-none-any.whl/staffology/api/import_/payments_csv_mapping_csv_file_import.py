from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/import/payments/mappings/{id}/csv".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
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
) -> Response[ReportResponse]:
    """Get PaymentsCsvMapping CSV File

     Gets a CSV file in the format needed to import for the specified PaymentsCsvMapping
    This is only available for PaymentsCsvMapping with a Type of ColumnBased

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
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
) -> Optional[ReportResponse]:
    """Get PaymentsCsvMapping CSV File

     Gets a CSV file in the format needed to import for the specified PaymentsCsvMapping
    This is only available for PaymentsCsvMapping with a Type of ColumnBased

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Response[ReportResponse]:
    """Get PaymentsCsvMapping CSV File

     Gets a CSV file in the format needed to import for the specified PaymentsCsvMapping
    This is only available for PaymentsCsvMapping with a Type of ColumnBased

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[ReportResponse]:
    """Get PaymentsCsvMapping CSV File

     Gets a CSV file in the format needed to import for the specified PaymentsCsvMapping
    This is only available for PaymentsCsvMapping with a Type of ColumnBased

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
        )
    ).parsed
