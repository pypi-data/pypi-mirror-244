from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_analysis_category_code_request import ContractAnalysisCategoryCodeRequest
from ...models.contract_analysis_category_code_response import ContractAnalysisCategoryCodeResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    analysis_category_id: str,
    code: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/analysiscategories/{analysisCategoryId}/categorycodes/{code}".format(
        client.base_url, employerId=employer_id, analysisCategoryId=analysis_category_id, code=code
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


def _parse_response(*, response: httpx.Response) -> Optional[ContractAnalysisCategoryCodeResponse]:
    if response.status_code == 200:
        response_200 = ContractAnalysisCategoryCodeResponse.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractAnalysisCategoryCodeResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    analysis_category_id: str,
    code: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Response[ContractAnalysisCategoryCodeResponse]:
    """Update AnalysisCategoryCode

     Updates the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        code (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[ContractAnalysisCategoryCodeResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        analysis_category_id=analysis_category_id,
        code=code,
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
    code: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Optional[ContractAnalysisCategoryCodeResponse]:
    """Update AnalysisCategoryCode

     Updates the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        code (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[ContractAnalysisCategoryCodeResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        analysis_category_id=analysis_category_id,
        code=code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    analysis_category_id: str,
    code: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Response[ContractAnalysisCategoryCodeResponse]:
    """Update AnalysisCategoryCode

     Updates the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        code (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[ContractAnalysisCategoryCodeResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        analysis_category_id=analysis_category_id,
        code=code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    analysis_category_id: str,
    code: str,
    *,
    client: Client,
    json_body: ContractAnalysisCategoryCodeRequest,
) -> Optional[ContractAnalysisCategoryCodeResponse]:
    """Update AnalysisCategoryCode

     Updates the details of an existing AnalysisCategoryCode.

    Args:
        employer_id (str):
        analysis_category_id (str):
        code (str):
        json_body (ContractAnalysisCategoryCodeRequest):

    Returns:
        Response[ContractAnalysisCategoryCodeResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            analysis_category_id=analysis_category_id,
            code=code,
            client=client,
            json_body=json_body,
        )
    ).parsed
