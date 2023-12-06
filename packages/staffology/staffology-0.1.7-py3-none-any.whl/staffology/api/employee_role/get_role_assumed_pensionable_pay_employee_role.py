import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.leave_pay_type import LeavePayType
from ...models.leave_type import LeaveType
from ...models.pay_periods import PayPeriods
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    role_id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    ssp_first_day: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/roles/{roleId}/assumedpensionablepay".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, roleId=role_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

    json_leave_type: Union[Unset, None, str] = UNSET
    if not isinstance(leave_type, Unset):
        json_leave_type = leave_type.value if leave_type else None

    params["leaveType"] = json_leave_type

    json_leave_pay_type: Union[Unset, None, str] = UNSET
    if not isinstance(leave_pay_type, Unset):
        json_leave_pay_type = leave_pay_type.value if leave_pay_type else None

    params["leavePayType"] = json_leave_pay_type

    json_ssp_first_day: Union[Unset, None, str] = UNSET
    if not isinstance(ssp_first_day, Unset):
        json_ssp_first_day = ssp_first_day.isoformat() if ssp_first_day else None

    params["sspFirstDay"] = json_ssp_first_day

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, float]]:
    if response.status_code == 200:
        response_200 = cast(float, response.json())
        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, float]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    role_id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    ssp_first_day: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, float]]:
    """Calculate Assumed Pensionable Pay

    Args:
        employer_id (str):
        employee_id (str):
        role_id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        ssp_first_day (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, float]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        role_id=role_id,
        client=client,
        pay_period=pay_period,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        ssp_first_day=ssp_first_day,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    role_id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    ssp_first_day: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, float]]:
    """Calculate Assumed Pensionable Pay

    Args:
        employer_id (str):
        employee_id (str):
        role_id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        ssp_first_day (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, float]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        role_id=role_id,
        client=client,
        pay_period=pay_period,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        ssp_first_day=ssp_first_day,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    role_id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    ssp_first_day: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, float]]:
    """Calculate Assumed Pensionable Pay

    Args:
        employer_id (str):
        employee_id (str):
        role_id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        ssp_first_day (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, float]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        role_id=role_id,
        client=client,
        pay_period=pay_period,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        ssp_first_day=ssp_first_day,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    role_id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    ssp_first_day: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, float]]:
    """Calculate Assumed Pensionable Pay

    Args:
        employer_id (str):
        employee_id (str):
        role_id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        ssp_first_day (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, float]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            role_id=role_id,
            client=client,
            pay_period=pay_period,
            leave_type=leave_type,
            leave_pay_type=leave_pay_type,
            ssp_first_day=ssp_first_day,
        )
    ).parsed
