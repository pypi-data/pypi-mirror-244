from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_working_pattern_request import ContractWorkingPatternRequest
from ...models.working_pattern import WorkingPattern
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: ContractWorkingPatternRequest,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/workingpatterns".format(
        client.base_url,employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, WorkingPattern]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 201:
        response_201 = WorkingPattern.from_dict(response.json())



        return response_201
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, WorkingPattern]]:
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
    json_body: ContractWorkingPatternRequest,

) -> Response[Union[Any, WorkingPattern]]:
    """Create WorkingPattern

     Creates a new WorkingPattern for the Employer.

    Args:
        employer_id (str):
        json_body (ContractWorkingPatternRequest):

    Returns:
        Response[Union[Any, WorkingPattern]]
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
    json_body: ContractWorkingPatternRequest,

) -> Optional[Union[Any, WorkingPattern]]:
    """Create WorkingPattern

     Creates a new WorkingPattern for the Employer.

    Args:
        employer_id (str):
        json_body (ContractWorkingPatternRequest):

    Returns:
        Response[Union[Any, WorkingPattern]]
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
    json_body: ContractWorkingPatternRequest,

) -> Response[Union[Any, WorkingPattern]]:
    """Create WorkingPattern

     Creates a new WorkingPattern for the Employer.

    Args:
        employer_id (str):
        json_body (ContractWorkingPatternRequest):

    Returns:
        Response[Union[Any, WorkingPattern]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
client=client,
json_body=json_body,

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
    json_body: ContractWorkingPatternRequest,

) -> Optional[Union[Any, WorkingPattern]]:
    """Create WorkingPattern

     Creates a new WorkingPattern for the Employer.

    Args:
        employer_id (str):
        json_body (ContractWorkingPatternRequest):

    Returns:
        Response[Union[Any, WorkingPattern]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
client=client,
json_body=json_body,

    )).parsed

