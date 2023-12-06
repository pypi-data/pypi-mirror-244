from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.cost_of_employment_report_report_response import CostOfEmploymentReportReportResponse
from ...models.pay_periods import PayPeriods
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
    ordinal: Union[Unset, None, int] = 1,
    accept: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/costofemployment".format(
        client.base_url,employerId=employer_id,taxYear=tax_year,payPeriod=pay_period)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept



    

    params: Dict[str, Any] = {}
    params["fromPeriod"] = from_period


    params["toPeriod"] = to_period


    params["ordinal"] = ordinal



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[CostOfEmploymentReportReportResponse]:
    if response.status_code == 200:
        response_200 = CostOfEmploymentReportReportResponse.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[CostOfEmploymentReportReportResponse]:
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
    ordinal: Union[Unset, None, int] = 1,
    accept: Union[Unset, str] = UNSET,

) -> Response[CostOfEmploymentReportReportResponse]:
    """Cost Of Employment

     Returns a report detailing the employment cost per employee for a payrun or range of payruns.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        accept (Union[Unset, str]):

    Returns:
        Response[CostOfEmploymentReportReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
ordinal=ordinal,
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
    ordinal: Union[Unset, None, int] = 1,
    accept: Union[Unset, str] = UNSET,

) -> Optional[CostOfEmploymentReportReportResponse]:
    """Cost Of Employment

     Returns a report detailing the employment cost per employee for a payrun or range of payruns.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        accept (Union[Unset, str]):

    Returns:
        Response[CostOfEmploymentReportReportResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
ordinal=ordinal,
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
    ordinal: Union[Unset, None, int] = 1,
    accept: Union[Unset, str] = UNSET,

) -> Response[CostOfEmploymentReportReportResponse]:
    """Cost Of Employment

     Returns a report detailing the employment cost per employee for a payrun or range of payruns.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        accept (Union[Unset, str]):

    Returns:
        Response[CostOfEmploymentReportReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
ordinal=ordinal,
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
    ordinal: Union[Unset, None, int] = 1,
    accept: Union[Unset, str] = UNSET,

) -> Optional[CostOfEmploymentReportReportResponse]:
    """Cost Of Employment

     Returns a report detailing the employment cost per employee for a payrun or range of payruns.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        accept (Union[Unset, str]):

    Returns:
        Response[CostOfEmploymentReportReportResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
client=client,
from_period=from_period,
to_period=to_period,
ordinal=ordinal,
accept=accept,

    )).parsed

