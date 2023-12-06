from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.processing_note import ProcessingNote
from ...models.processing_note_status import ProcessingNoteStatus
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    json_body: ProcessingNoteStatus,
    ordinal: Union[Unset, None, int] = 1,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/processingnotes/{id}/status".format(
        client.base_url,employerId=employer_id,taxYear=tax_year,payPeriod=pay_period,periodNumber=period_number,id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    json_json_body = json_body.value



    

    return {
	    "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ProcessingNote]]:
    if response.status_code == 200:
        response_200 = ProcessingNote.from_dict(response.json())



        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ProcessingNote]]:
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
    id: str,
    *,
    client: Client,
    json_body: ProcessingNoteStatus,
    ordinal: Union[Unset, None, int] = 1,

) -> Response[Union[Any, ProcessingNote]]:
    """Set a ProcessingNote status

     Set a ProcessingNote status.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNoteStatus):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
id=id,
client=client,
json_body=json_body,
ordinal=ordinal,

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
    id: str,
    *,
    client: Client,
    json_body: ProcessingNoteStatus,
    ordinal: Union[Unset, None, int] = 1,

) -> Optional[Union[Any, ProcessingNote]]:
    """Set a ProcessingNote status

     Set a ProcessingNote status.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNoteStatus):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
id=id,
client=client,
json_body=json_body,
ordinal=ordinal,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    json_body: ProcessingNoteStatus,
    ordinal: Union[Unset, None, int] = 1,

) -> Response[Union[Any, ProcessingNote]]:
    """Set a ProcessingNote status

     Set a ProcessingNote status.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNoteStatus):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
id=id,
client=client,
json_body=json_body,
ordinal=ordinal,

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
    id: str,
    *,
    client: Client,
    json_body: ProcessingNoteStatus,
    ordinal: Union[Unset, None, int] = 1,

) -> Optional[Union[Any, ProcessingNote]]:
    """Set a ProcessingNote status

     Set a ProcessingNote status.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNoteStatus):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
id=id,
client=client,
json_body=json_body,
ordinal=ordinal,

    )).parsed

