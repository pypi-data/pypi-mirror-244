from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_run_entry import PayRunEntry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    is_closed: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/employees/{employeeId}/Last".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["isClosed"] = is_closed

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayRunEntry]:
    if response.status_code == 200:
        response_200 = PayRunEntry.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[PayRunEntry]:
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
    is_closed: Union[Unset, None, bool] = UNSET,
) -> Response[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        is_closed (Union[Unset, None, bool]):

    Returns:
        Response[PayRunEntry]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        is_closed=is_closed,
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
    is_closed: Union[Unset, None, bool] = UNSET,
) -> Optional[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        is_closed (Union[Unset, None, bool]):

    Returns:
        Response[PayRunEntry]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        is_closed=is_closed,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    is_closed: Union[Unset, None, bool] = UNSET,
) -> Response[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        is_closed (Union[Unset, None, bool]):

    Returns:
        Response[PayRunEntry]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        is_closed=is_closed,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    is_closed: Union[Unset, None, bool] = UNSET,
) -> Optional[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        is_closed (Union[Unset, None, bool]):

    Returns:
        Response[PayRunEntry]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            is_closed=is_closed,
        )
    ).parsed
