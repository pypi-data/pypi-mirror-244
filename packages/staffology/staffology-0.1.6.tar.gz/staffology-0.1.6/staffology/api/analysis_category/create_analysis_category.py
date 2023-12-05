from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_analysis_category_request import ContractAnalysisCategoryRequest
from ...models.contract_analysis_category_response import ContractAnalysisCategoryResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryRequest,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/analysiscategories".format(client.base_url, employerId=employer_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractAnalysisCategoryResponse]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 201:
        response_201 = ContractAnalysisCategoryResponse.from_dict(response.json())

        return response_201
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractAnalysisCategoryResponse]]:
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
    json_body: ContractAnalysisCategoryRequest,
) -> Response[Union[Any, ContractAnalysisCategoryResponse]]:
    """Create AnalysisCategory

     Create a new AnalysisCategory for the Employer.

    Args:
        employer_id (str):
        json_body (ContractAnalysisCategoryRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryResponse]]
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
    json_body: ContractAnalysisCategoryRequest,
) -> Optional[Union[Any, ContractAnalysisCategoryResponse]]:
    """Create AnalysisCategory

     Create a new AnalysisCategory for the Employer.

    Args:
        employer_id (str):
        json_body (ContractAnalysisCategoryRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryResponse]]
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
    json_body: ContractAnalysisCategoryRequest,
) -> Response[Union[Any, ContractAnalysisCategoryResponse]]:
    """Create AnalysisCategory

     Create a new AnalysisCategory for the Employer.

    Args:
        employer_id (str):
        json_body (ContractAnalysisCategoryRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryResponse]]
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
    json_body: ContractAnalysisCategoryRequest,
) -> Optional[Union[Any, ContractAnalysisCategoryResponse]]:
    """Create AnalysisCategory

     Create a new AnalysisCategory for the Employer.

    Args:
        employer_id (str):
        json_body (ContractAnalysisCategoryRequest):

    Returns:
        Response[Union[Any, ContractAnalysisCategoryResponse]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
