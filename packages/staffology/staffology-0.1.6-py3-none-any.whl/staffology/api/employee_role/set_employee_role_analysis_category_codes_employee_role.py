from typing import Any, Dict, List, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_employee_role_analysis_category_code_request import (
    ContractEmployeeRoleAnalysisCategoryCodeRequest,
)
from ...models.contract_employee_role_analysis_category_code_response import (
    ContractEmployeeRoleAnalysisCategoryCodeResponse,
)
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: List[ContractEmployeeRoleAnalysisCategoryCodeRequest],
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/roles/{id}/analysiscategories/{analysisCategoryId}/analysiscategorycodes".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, id=id, analysisCategoryId=analysis_category_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ContractEmployeeRoleAnalysisCategoryCodeResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
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
    analysis_category_id: str,
    *,
    client: Client,
    json_body: List[ContractEmployeeRoleAnalysisCategoryCodeRequest],
) -> Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
    """Set  Employee Role AnalysisCategorycode

     Assigns AnalysisCategoryCode to an Employee Role.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        analysis_category_id (str):
        json_body (List[ContractEmployeeRoleAnalysisCategoryCodeRequest]):

    Returns:
        Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        analysis_category_id=analysis_category_id,
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
    employee_id: str,
    id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: List[ContractEmployeeRoleAnalysisCategoryCodeRequest],
) -> Optional[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
    """Set  Employee Role AnalysisCategorycode

     Assigns AnalysisCategoryCode to an Employee Role.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        analysis_category_id (str):
        json_body (List[ContractEmployeeRoleAnalysisCategoryCodeRequest]):

    Returns:
        Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        analysis_category_id=analysis_category_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: List[ContractEmployeeRoleAnalysisCategoryCodeRequest],
) -> Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
    """Set  Employee Role AnalysisCategorycode

     Assigns AnalysisCategoryCode to an Employee Role.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        analysis_category_id (str):
        json_body (List[ContractEmployeeRoleAnalysisCategoryCodeRequest]):

    Returns:
        Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        analysis_category_id=analysis_category_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: List[ContractEmployeeRoleAnalysisCategoryCodeRequest],
) -> Optional[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]:
    """Set  Employee Role AnalysisCategorycode

     Assigns AnalysisCategoryCode to an Employee Role.
    You must have the multi-role feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        analysis_category_id (str):
        json_body (List[ContractEmployeeRoleAnalysisCategoryCodeRequest]):

    Returns:
        Response[Union[Any, List[ContractEmployeeRoleAnalysisCategoryCodeResponse]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            id=id,
            analysis_category_id=analysis_category_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
