import datetime
from typing import Any, Dict, Optional, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    start_date: datetime.datetime,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/employees/{employeeId}/averageholidaypayrate".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_start_date = start_date.isoformat()

    params["startDate"] = json_start_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[float]:
    if response.status_code == 200:
        response_200 = cast(float, response.json())
        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[float]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    start_date: datetime.datetime,
) -> Response[float]:
    """Calculate Average Holiday Pay Rate

     Calculates the average holiday pay rate for an employee based on their holiday scheme configuration

    Args:
        employer_id (str):
        employee_id (str):
        start_date (datetime.datetime):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        start_date=start_date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    start_date: datetime.datetime,
) -> Optional[float]:
    """Calculate Average Holiday Pay Rate

     Calculates the average holiday pay rate for an employee based on their holiday scheme configuration

    Args:
        employer_id (str):
        employee_id (str):
        start_date (datetime.datetime):

    Returns:
        Response[float]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        start_date=start_date,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    start_date: datetime.datetime,
) -> Response[float]:
    """Calculate Average Holiday Pay Rate

     Calculates the average holiday pay rate for an employee based on their holiday scheme configuration

    Args:
        employer_id (str):
        employee_id (str):
        start_date (datetime.datetime):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        start_date=start_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    start_date: datetime.datetime,
) -> Optional[float]:
    """Calculate Average Holiday Pay Rate

     Calculates the average holiday pay rate for an employee based on their holiday scheme configuration

    Args:
        employer_id (str):
        employee_id (str):
        start_date (datetime.datetime):

    Returns:
        Response[float]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            start_date=start_date,
        )
    ).parsed
