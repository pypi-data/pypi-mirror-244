from typing import Any, Dict, List, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.item import Item
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    payrun_entry_id: Union[Unset, None, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/processingnotes".format(
        client.base_url,employerId=employer_id,taxYear=tax_year,payPeriod=pay_period,periodNumber=period_number)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal


    params["payrunEntryId"] = payrun_entry_id



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[Item]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = Item.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[List[Item]]:
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
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    payrun_entry_id: Union[Unset, None, str] = UNSET,

) -> Response[List[Item]]:
    """List ProcessingNotes for a PayRun

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payrun_entry_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
ordinal=ordinal,
payrun_entry_id=payrun_entry_id,

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
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    payrun_entry_id: Union[Unset, None, str] = UNSET,

) -> Optional[List[Item]]:
    """List ProcessingNotes for a PayRun

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payrun_entry_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
ordinal=ordinal,
payrun_entry_id=payrun_entry_id,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    payrun_entry_id: Union[Unset, None, str] = UNSET,

) -> Response[List[Item]]:
    """List ProcessingNotes for a PayRun

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payrun_entry_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
ordinal=ordinal,
payrun_entry_id=payrun_entry_id,

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
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    payrun_entry_id: Union[Unset, None, str] = UNSET,

) -> Optional[List[Item]]:
    """List ProcessingNotes for a PayRun

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payrun_entry_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
ordinal=ordinal,
payrun_entry_id=payrun_entry_id,

    )).parsed

