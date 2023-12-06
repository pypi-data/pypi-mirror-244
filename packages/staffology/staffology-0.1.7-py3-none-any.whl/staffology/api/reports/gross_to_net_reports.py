from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.gross_to_net_report_report_response import GrossToNetReportReportResponse
from ...models.pay_periods import PayPeriods
from ...models.report_sort_by import ReportSortBy
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, ReportSortBy] = UNSET,
    sort_descending: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    for_cis: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/gross-to-net".format(
        client.base_url,employerId=employer_id,taxYear=tax_year,payPeriod=pay_period)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept



    

    params: Dict[str, Any] = {}
    params["fromPeriod"] = from_period


    params["toPeriod"] = to_period


    json_sort_by: Union[Unset, None, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value if sort_by else None

    params["sortBy"] = json_sort_by


    params["sortDescending"] = sort_descending


    params["ordinal"] = ordinal


    params["forCis"] = for_cis



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[GrossToNetReportReportResponse]:
    if response.status_code == 200:
        response_200 = GrossToNetReportReportResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[GrossToNetReportReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, ReportSortBy] = UNSET,
    sort_descending: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    for_cis: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[GrossToNetReportReportResponse]:
    """Gross To Net

     Returns a report comparing employees' gross pay with their net pay for one or more pay periods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        sort_by (Union[Unset, None, ReportSortBy]):
        sort_descending (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        for_cis (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[GrossToNetReportReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
sort_by=sort_by,
sort_descending=sort_descending,
ordinal=ordinal,
for_cis=for_cis,
accept=accept,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, ReportSortBy] = UNSET,
    sort_descending: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    for_cis: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[GrossToNetReportReportResponse]:
    """Gross To Net

     Returns a report comparing employees' gross pay with their net pay for one or more pay periods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        sort_by (Union[Unset, None, ReportSortBy]):
        sort_descending (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        for_cis (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[GrossToNetReportReportResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
sort_by=sort_by,
sort_descending=sort_descending,
ordinal=ordinal,
for_cis=for_cis,
accept=accept,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, ReportSortBy] = UNSET,
    sort_descending: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    for_cis: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[GrossToNetReportReportResponse]:
    """Gross To Net

     Returns a report comparing employees' gross pay with their net pay for one or more pay periods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        sort_by (Union[Unset, None, ReportSortBy]):
        sort_descending (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        for_cis (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[GrossToNetReportReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
sort_by=sort_by,
sort_descending=sort_descending,
ordinal=ordinal,
for_cis=for_cis,
accept=accept,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    sort_by: Union[Unset, None, ReportSortBy] = UNSET,
    sort_descending: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    for_cis: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[GrossToNetReportReportResponse]:
    """Gross To Net

     Returns a report comparing employees' gross pay with their net pay for one or more pay periods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        sort_by (Union[Unset, None, ReportSortBy]):
        sort_descending (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        for_cis (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[GrossToNetReportReportResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
sort_by=sort_by,
sort_descending=sort_descending,
ordinal=ordinal,
for_cis=for_cis,
accept=accept,

    )).parsed

