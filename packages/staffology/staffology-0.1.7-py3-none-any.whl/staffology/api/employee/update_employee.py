from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_employee_response import ContractEmployeeResponse
from ...models.contract_update_employee_request import ContractUpdateEmployeeRequest
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: ContractUpdateEmployeeRequest,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}".format(client.base_url, employerId=employer_id, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractEmployeeResponse]]:
    if response.status_code == 200:
        response_200 = ContractEmployeeResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractEmployeeResponse]]:
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
    json_body: ContractUpdateEmployeeRequest,
) -> Response[Union[Any, ContractEmployeeResponse]]:
    """Update an Employee

    Args:
        employer_id (str):
        id (str):
        json_body (ContractUpdateEmployeeRequest):

    Returns:
        Response[Union[Any, ContractEmployeeResponse]]
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
    json_body: ContractUpdateEmployeeRequest,
) -> Optional[Union[Any, ContractEmployeeResponse]]:
    """Update an Employee

    Args:
        employer_id (str):
        id (str):
        json_body (ContractUpdateEmployeeRequest):

    Returns:
        Response[Union[Any, ContractEmployeeResponse]]
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
    json_body: ContractUpdateEmployeeRequest,
) -> Response[Union[Any, ContractEmployeeResponse]]:
    """Update an Employee

    Args:
        employer_id (str):
        id (str):
        json_body (ContractUpdateEmployeeRequest):

    Returns:
        Response[Union[Any, ContractEmployeeResponse]]
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
    json_body: ContractUpdateEmployeeRequest,
) -> Optional[Union[Any, ContractEmployeeResponse]]:
    """Update an Employee

    Args:
        employer_id (str):
        id (str):
        json_body (ContractUpdateEmployeeRequest):

    Returns:
        Response[Union[Any, ContractEmployeeResponse]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
