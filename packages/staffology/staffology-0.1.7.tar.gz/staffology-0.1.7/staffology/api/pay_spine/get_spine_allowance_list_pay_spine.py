from typing import Any, Dict, List, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.spine_allowance import SpineAllowance
from ...types import Response


def _get_kwargs(
    employer_id: str,
    pay_spine_id: str,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payspines/{paySpineId}/allowances".format(
        client.base_url,employerId=employer_id,paySpineId=pay_spine_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[SpineAllowance]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = SpineAllowance.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[SpineAllowance]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_spine_id: str,
    *,
    client: Client,

) -> Response[Union[Any, List[SpineAllowance]]]:
    """List SpineAllowances

     List Allowances for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):

    Returns:
        Response[Union[Any, List[SpineAllowance]]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
client=client,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    employer_id: str,
    pay_spine_id: str,
    *,
    client: Client,

) -> Optional[Union[Any, List[SpineAllowance]]]:
    """List SpineAllowances

     List Allowances for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):

    Returns:
        Response[Union[Any, List[SpineAllowance]]]
    """


    return sync_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
client=client,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    pay_spine_id: str,
    *,
    client: Client,

) -> Response[Union[Any, List[SpineAllowance]]]:
    """List SpineAllowances

     List Allowances for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):

    Returns:
        Response[Union[Any, List[SpineAllowance]]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    employer_id: str,
    pay_spine_id: str,
    *,
    client: Client,

) -> Optional[Union[Any, List[SpineAllowance]]]:
    """List SpineAllowances

     List Allowances for a Pay Spine

    Args:
        employer_id (str):
        pay_spine_id (str):

    Returns:
        Response[Union[Any, List[SpineAllowance]]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
pay_spine_id=pay_spine_id,
client=client,

    )).parsed

