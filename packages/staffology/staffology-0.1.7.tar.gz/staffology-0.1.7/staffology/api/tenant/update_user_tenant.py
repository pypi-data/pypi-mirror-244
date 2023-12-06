from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: User,

) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/{userId}".format(
        client.base_url,id=id,userId=user_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, User]]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())



        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, User]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: User,

) -> Response[Union[Any, User]]:
    """Update a User

     Set the details of a User that belongs to the Tenant

    Args:
        id (str):
        user_id (str):
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[Union[Any, User]]
    """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: User,

) -> Optional[Union[Any, User]]:
    """Update a User

     Set the details of a User that belongs to the Tenant

    Args:
        id (str):
        user_id (str):
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[Union[Any, User]]
    """


    return sync_detailed(
        id=id,
user_id=user_id,
client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: User,

) -> Response[Union[Any, User]]:
    """Update a User

     Set the details of a User that belongs to the Tenant

    Args:
        id (str):
        user_id (str):
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[Union[Any, User]]
    """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: User,

) -> Optional[Union[Any, User]]:
    """Update a User

     Set the details of a User that belongs to the Tenant

    Args:
        id (str):
        user_id (str):
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[Union[Any, User]]
    """


    return (await asyncio_detailed(
        id=id,
user_id=user_id,
client=client,
json_body=json_body,

    )).parsed

