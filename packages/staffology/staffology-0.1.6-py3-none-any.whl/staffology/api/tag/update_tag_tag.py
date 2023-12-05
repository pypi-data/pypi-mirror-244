from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.tag import Tag
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: Tag,
    code: Union[Unset, None, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/tags/tag".format(
        client.base_url,employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["code"] = code



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    json_json_body = json_body.to_dict()



    

    return {
	    "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Tag]]:
    if response.status_code == 200:
        response_200 = Tag.from_dict(response.json())



        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Tag]]:
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
    json_body: Tag,
    code: Union[Unset, None, str] = UNSET,

) -> Response[Union[Any, Tag]]:
    """Update Tag

     Updates the details of an existing Tag.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):
        json_body (Tag):

    Returns:
        Response[Union[Any, Tag]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
client=client,
json_body=json_body,
code=code,

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
    json_body: Tag,
    code: Union[Unset, None, str] = UNSET,

) -> Optional[Union[Any, Tag]]:
    """Update Tag

     Updates the details of an existing Tag.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):
        json_body (Tag):

    Returns:
        Response[Union[Any, Tag]]
    """


    return sync_detailed(
        employer_id=employer_id,
client=client,
json_body=json_body,
code=code,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: Tag,
    code: Union[Unset, None, str] = UNSET,

) -> Response[Union[Any, Tag]]:
    """Update Tag

     Updates the details of an existing Tag.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):
        json_body (Tag):

    Returns:
        Response[Union[Any, Tag]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
client=client,
json_body=json_body,
code=code,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    employer_id: str,
    *,
    client: Client,
    json_body: Tag,
    code: Union[Unset, None, str] = UNSET,

) -> Optional[Union[Any, Tag]]:
    """Update Tag

     Updates the details of an existing Tag.

    Args:
        employer_id (str):
        code (Union[Unset, None, str]):
        json_body (Tag):

    Returns:
        Response[Union[Any, Tag]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
client=client,
json_body=json_body,
code=code,

    )).parsed

