from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_gross_to_net_report_request import ContractGrossToNetReportRequest
from ...models.contract_job_response import ContractJobResponse
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: ContractGrossToNetReportRequest,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/async/gross-to-net".format(client.base_url, employerId=employer_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ContractJobResponse]]:
    if response.status_code == 202:
        response_202 = ContractJobResponse.from_dict(response.json())

        return response_202
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ContractJobResponse]]:
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
    json_body: ContractGrossToNetReportRequest,
) -> Response[Union[Any, ContractJobResponse]]:
    """Gross To Net async

     Returns a job that is created to process a report comparing employees' gross pay with their net pay
    for one or more pay periods.
    Use the GET of Jobs to get the status and response of the job..

    Args:
        employer_id (str):
        json_body (ContractGrossToNetReportRequest):

    Returns:
        Response[Union[Any, ContractJobResponse]]
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
    json_body: ContractGrossToNetReportRequest,
) -> Optional[Union[Any, ContractJobResponse]]:
    """Gross To Net async

     Returns a job that is created to process a report comparing employees' gross pay with their net pay
    for one or more pay periods.
    Use the GET of Jobs to get the status and response of the job..

    Args:
        employer_id (str):
        json_body (ContractGrossToNetReportRequest):

    Returns:
        Response[Union[Any, ContractJobResponse]]
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
    json_body: ContractGrossToNetReportRequest,
) -> Response[Union[Any, ContractJobResponse]]:
    """Gross To Net async

     Returns a job that is created to process a report comparing employees' gross pay with their net pay
    for one or more pay periods.
    Use the GET of Jobs to get the status and response of the job..

    Args:
        employer_id (str):
        json_body (ContractGrossToNetReportRequest):

    Returns:
        Response[Union[Any, ContractJobResponse]]
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
    json_body: ContractGrossToNetReportRequest,
) -> Optional[Union[Any, ContractJobResponse]]:
    """Gross To Net async

     Returns a job that is created to process a report comparing employees' gross pay with their net pay
    for one or more pay periods.
    Use the GET of Jobs to get the status and response of the job..

    Args:
        employer_id (str):
        json_body (ContractGrossToNetReportRequest):

    Returns:
        Response[Union[Any, ContractJobResponse]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
