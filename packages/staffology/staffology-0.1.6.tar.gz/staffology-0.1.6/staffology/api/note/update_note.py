from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.note import Note
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
    json_body: Note,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/notes/{id}".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, id=id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Note]]:
    if response.status_code == 200:
        response_200 = Note.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Note]]:
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
    *,
    client: Client,
    json_body: Note,
) -> Response[Union[Any, Note]]:
    """Update Note

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        json_body (Note): Used to represent a Note for an Employee

    Returns:
        Response[Union[Any, Note]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
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
    employee_id: str,
    id: str,
    *,
    client: Client,
    json_body: Note,
) -> Optional[Union[Any, Note]]:
    """Update Note

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        json_body (Note): Used to represent a Note for an Employee

    Returns:
        Response[Union[Any, Note]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
    json_body: Note,
) -> Response[Union[Any, Note]]:
    """Update Note

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        json_body (Note): Used to represent a Note for an Employee

    Returns:
        Response[Union[Any, Note]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
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
    *,
    client: Client,
    json_body: Note,
) -> Optional[Union[Any, Note]]:
    """Update Note

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        json_body (Note): Used to represent a Note for an Employee

    Returns:
        Response[Union[Any, Note]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
