import datetime
from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.change_summary_list_report_response import ChangeSummaryListReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    accept: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/changes".format(
        client.base_url,employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept



    

    params: Dict[str, Any] = {}
    json_from_date: Union[Unset, None, str] = UNSET
    if not isinstance(from_date, Unset):
        json_from_date = from_date.isoformat() if from_date else None

    params["fromDate"] = json_from_date


    json_to_date: Union[Unset, None, str] = UNSET
    if not isinstance(to_date, Unset):
        json_to_date = to_date.isoformat() if to_date else None

    params["toDate"] = json_to_date



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ChangeSummaryListReportResponse]:
    if response.status_code == 200:
        response_200 = ChangeSummaryListReportResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ChangeSummaryListReportResponse]:
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
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    accept: Union[Unset, str] = UNSET,

) -> Response[ChangeSummaryListReportResponse]:
    """Gets audit changes of all employees within a company.

    Args:
        employer_id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        accept (Union[Unset, str]):

    Returns:
        Response[ChangeSummaryListReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
client=client,
from_date=from_date,
to_date=to_date,
accept=accept,

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
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ChangeSummaryListReportResponse]:
    """Gets audit changes of all employees within a company.

    Args:
        employer_id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        accept (Union[Unset, str]):

    Returns:
        Response[ChangeSummaryListReportResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
client=client,
from_date=from_date,
to_date=to_date,
accept=accept,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    accept: Union[Unset, str] = UNSET,

) -> Response[ChangeSummaryListReportResponse]:
    """Gets audit changes of all employees within a company.

    Args:
        employer_id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        accept (Union[Unset, str]):

    Returns:
        Response[ChangeSummaryListReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
client=client,
from_date=from_date,
to_date=to_date,
accept=accept,

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
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ChangeSummaryListReportResponse]:
    """Gets audit changes of all employees within a company.

    Args:
        employer_id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        accept (Union[Unset, str]):

    Returns:
        Response[ChangeSummaryListReportResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
client=client,
from_date=from_date,
to_date=to_date,
accept=accept,

    )).parsed

