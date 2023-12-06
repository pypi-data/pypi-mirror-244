from typing import Any, Dict, List, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.item import Item
from ...models.occupational_sick_leave_history import OccupationalSickLeaveHistory
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: List[OccupationalSickLeaveHistory],
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/occupationalsickleaveshistory/import".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[Item]]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = Item.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[Item]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: List[OccupationalSickLeaveHistory],
) -> Response[Union[Any, List[Item]]]:
    """Upload Occupational Sick Leave History

     Upload new Occupational sick leave history for the Employer against specific occupational policy.

    Args:
        employer_id (str):
        json_body (List[OccupationalSickLeaveHistory]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    *,
    client: Client,
    json_body: List[OccupationalSickLeaveHistory],
) -> Optional[Union[Any, List[Item]]]:
    """Upload Occupational Sick Leave History

     Upload new Occupational sick leave history for the Employer against specific occupational policy.

    Args:
        employer_id (str):
        json_body (List[OccupationalSickLeaveHistory]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: List[OccupationalSickLeaveHistory],
) -> Response[Union[Any, List[Item]]]:
    """Upload Occupational Sick Leave History

     Upload new Occupational sick leave history for the Employer against specific occupational policy.

    Args:
        employer_id (str):
        json_body (List[OccupationalSickLeaveHistory]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    json_body: List[OccupationalSickLeaveHistory],
) -> Optional[Union[Any, List[Item]]]:
    """Upload Occupational Sick Leave History

     Upload new Occupational sick leave history for the Employer against specific occupational policy.

    Args:
        employer_id (str):
        json_body (List[OccupationalSickLeaveHistory]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
