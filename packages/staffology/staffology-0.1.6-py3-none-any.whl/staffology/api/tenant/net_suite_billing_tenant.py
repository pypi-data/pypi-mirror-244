from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    year: Union[Unset, None, int] = UNSET,
    month: Union[Unset, None, int] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/tenants/{id}/reports/netsuitebills".format(
        client.base_url,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept



    

    params: Dict[str, Any] = {}
    params["year"] = year


    params["month"] = month


    params["allTenants"] = all_tenants



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    id: str,
    *,
    client: Client,
    year: Union[Unset, None, int] = UNSET,
    month: Union[Unset, None, int] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[ReportResponse]:
    """NetSuite Billing Report

     Returns a report detailing billing, for NetSuite, for the given year and month
    Only available to SuperAdmins

    Args:
        id (str):
        year (Union[Unset, None, int]):
        month (Union[Unset, None, int]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
year=year,
month=month,
all_tenants=all_tenants,
accept=accept,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    id: str,
    *,
    client: Client,
    year: Union[Unset, None, int] = UNSET,
    month: Union[Unset, None, int] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ReportResponse]:
    """NetSuite Billing Report

     Returns a report detailing billing, for NetSuite, for the given year and month
    Only available to SuperAdmins

    Args:
        id (str):
        year (Union[Unset, None, int]):
        month (Union[Unset, None, int]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    return sync_detailed(
        id=id,
client=client,
year=year,
month=month,
all_tenants=all_tenants,
accept=accept,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    year: Union[Unset, None, int] = UNSET,
    month: Union[Unset, None, int] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[ReportResponse]:
    """NetSuite Billing Report

     Returns a report detailing billing, for NetSuite, for the given year and month
    Only available to SuperAdmins

    Args:
        id (str):
        year (Union[Unset, None, int]):
        month (Union[Unset, None, int]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    kwargs = _get_kwargs(
        id=id,
client=client,
year=year,
month=month,
all_tenants=all_tenants,
accept=accept,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    id: str,
    *,
    client: Client,
    year: Union[Unset, None, int] = UNSET,
    month: Union[Unset, None, int] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ReportResponse]:
    """NetSuite Billing Report

     Returns a report detailing billing, for NetSuite, for the given year and month
    Only available to SuperAdmins

    Args:
        id (str):
        year (Union[Unset, None, int]):
        month (Union[Unset, None, int]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    return (await asyncio_detailed(
        id=id,
client=client,
year=year,
month=month,
all_tenants=all_tenants,
accept=accept,

    )).parsed

