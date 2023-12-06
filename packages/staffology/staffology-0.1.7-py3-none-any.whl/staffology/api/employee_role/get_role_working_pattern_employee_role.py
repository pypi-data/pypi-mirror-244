from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.employee_role_working_pattern import EmployeeRoleWorkingPattern
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    id: str,
    role_working_pattern_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/roles/{id}/workingpatterns/{roleWorkingPatternId}".format(
        client.base_url,
        employerId=employer_id,
        employeeId=employee_id,
        id=id,
        roleWorkingPatternId=role_working_pattern_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, EmployeeRoleWorkingPattern]]:
    if response.status_code == 200:
        response_200 = EmployeeRoleWorkingPattern.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, EmployeeRoleWorkingPattern]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    role_working_pattern_id: str,
    *,
    client: Client,
) -> Response[Union[Any, EmployeeRoleWorkingPattern]]:
    """Get Employee Role Working Pattern

     Gets the Employee Role Working Pattern specified.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        role_working_pattern_id (str):

    Returns:
        Response[Union[Any, EmployeeRoleWorkingPattern]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        role_working_pattern_id=role_working_pattern_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    id: str,
    role_working_pattern_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, EmployeeRoleWorkingPattern]]:
    """Get Employee Role Working Pattern

     Gets the Employee Role Working Pattern specified.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        role_working_pattern_id (str):

    Returns:
        Response[Union[Any, EmployeeRoleWorkingPattern]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        role_working_pattern_id=role_working_pattern_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    role_working_pattern_id: str,
    *,
    client: Client,
) -> Response[Union[Any, EmployeeRoleWorkingPattern]]:
    """Get Employee Role Working Pattern

     Gets the Employee Role Working Pattern specified.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        role_working_pattern_id (str):

    Returns:
        Response[Union[Any, EmployeeRoleWorkingPattern]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        role_working_pattern_id=role_working_pattern_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    id: str,
    role_working_pattern_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, EmployeeRoleWorkingPattern]]:
    """Get Employee Role Working Pattern

     Gets the Employee Role Working Pattern specified.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        role_working_pattern_id (str):

    Returns:
        Response[Union[Any, EmployeeRoleWorkingPattern]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            id=id,
            role_working_pattern_id=role_working_pattern_id,
            client=client,
        )
    ).parsed
