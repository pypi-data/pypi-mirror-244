from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/autoenrolment/assessments/{id}/letter".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
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
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Get Letter

     Returns either a PDF or HTML (depending on accept header) of the letter that needs to be sent to an
    employee as a result of the assessment.
    The same ReportResponse model that is used for reports is used here.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
        accept=accept,
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
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Get Letter

     Returns either a PDF or HTML (depending on accept header) of the letter that needs to be sent to an
    employee as a result of the assessment.
    The same ReportResponse model that is used for reports is used here.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Get Letter

     Returns either a PDF or HTML (depending on accept header) of the letter that needs to be sent to an
    employee as a result of the assessment.
    The same ReportResponse model that is used for reports is used here.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
        accept=accept,
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
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Get Letter

     Returns either a PDF or HTML (depending on accept header) of the letter that needs to be sent to an
    employee as a result of the assessment.
    The same ReportResponse model that is used for reports is used here.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            id=id,
            client=client,
            accept=accept,
        )
    ).parsed
