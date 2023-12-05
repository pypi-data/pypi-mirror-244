from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_analysis_category_code_request import ContractAnalysisCategoryCodeRequest
from ...models.contract_analysis_category_code_response import ContractAnalysisCategoryCodeResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/analysiscategories/{analysisCategoryId}/categorycodes".format(
        client.base_url, employerId=employer_id, analysisCategoryId=analysis_category_id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 201:
        response_201 = ContractAnalysisCategoryCodeResponse.from_dict(response.json())

        return response_201
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Response[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    """Create AnalysisCategoryCode

     Create the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryCodeResponse]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    analysis_category_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Optional[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    """Create AnalysisCategoryCode

     Create the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryCodeResponse]]
    """

    return sync_detailed(
        employer_id=employer_id,
        analysis_category_id=analysis_category_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Response[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    """Create AnalysisCategoryCode

     Create the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryCodeResponse]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        analysis_category_id=analysis_category_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    analysis_category_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Optional[Union[Any, ContractAnalysisCategoryCodeResponse]]:
    """Create AnalysisCategoryCode

     Create the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryCodeResponse]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            analysis_category_id=analysis_category_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
