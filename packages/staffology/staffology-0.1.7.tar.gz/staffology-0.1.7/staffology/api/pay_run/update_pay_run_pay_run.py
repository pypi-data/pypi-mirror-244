import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_run import PayRun
from ...models.pay_run_state_change import PayRunStateChange
from ...models.payslip_release_type import PayslipReleaseType
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
    payslip_release_type: Union[Unset, None, PayslipReleaseType] = UNSET,
    payslip_scheduled_date_time: Union[Unset, None, datetime.datetime] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}".format(
        client.base_url,employerId=employer_id,taxYear=tax_year,payPeriod=pay_period,periodNumber=period_number)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal


    params["sendPayslipEmails"] = send_payslip_emails


    json_payslip_release_type: Union[Unset, None, str] = UNSET
    if not isinstance(payslip_release_type, Unset):
        json_payslip_release_type = payslip_release_type.value if payslip_release_type else None

    params["payslipReleaseType"] = json_payslip_release_type


    json_payslip_scheduled_date_time: Union[Unset, None, str] = UNSET
    if not isinstance(payslip_scheduled_date_time, Unset):
        json_payslip_scheduled_date_time = payslip_scheduled_date_time.isoformat() if payslip_scheduled_date_time else None

    params["payslipScheduledDateTime"] = json_payslip_scheduled_date_time



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    json_json_body = json_body.to_dict()



    

    return {
	    "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PayRun]]:
    if response.status_code == 200:
        response_200 = PayRun.from_dict(response.json())



        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PayRun]]:
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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
    payslip_release_type: Union[Unset, None, PayslipReleaseType] = UNSET,
    payslip_scheduled_date_time: Union[Unset, None, datetime.datetime] = UNSET,

) -> Response[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        payslip_release_type (Union[Unset, None, PayslipReleaseType]):
        payslip_scheduled_date_time (Union[Unset, None, datetime.datetime]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
json_body=json_body,
ordinal=ordinal,
send_payslip_emails=send_payslip_emails,
payslip_release_type=payslip_release_type,
payslip_scheduled_date_time=payslip_scheduled_date_time,

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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
    payslip_release_type: Union[Unset, None, PayslipReleaseType] = UNSET,
    payslip_scheduled_date_time: Union[Unset, None, datetime.datetime] = UNSET,

) -> Optional[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        payslip_release_type (Union[Unset, None, PayslipReleaseType]):
        payslip_scheduled_date_time (Union[Unset, None, datetime.datetime]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
json_body=json_body,
ordinal=ordinal,
send_payslip_emails=send_payslip_emails,
payslip_release_type=payslip_release_type,
payslip_scheduled_date_time=payslip_scheduled_date_time,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
    payslip_release_type: Union[Unset, None, PayslipReleaseType] = UNSET,
    payslip_scheduled_date_time: Union[Unset, None, datetime.datetime] = UNSET,

) -> Response[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        payslip_release_type (Union[Unset, None, PayslipReleaseType]):
        payslip_scheduled_date_time (Union[Unset, None, datetime.datetime]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
json_body=json_body,
ordinal=ordinal,
send_payslip_emails=send_payslip_emails,
payslip_release_type=payslip_release_type,
payslip_scheduled_date_time=payslip_scheduled_date_time,

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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
    payslip_release_type: Union[Unset, None, PayslipReleaseType] = UNSET,
    payslip_scheduled_date_time: Union[Unset, None, datetime.datetime] = UNSET,

) -> Optional[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        payslip_release_type (Union[Unset, None, PayslipReleaseType]):
        payslip_scheduled_date_time (Union[Unset, None, datetime.datetime]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
pay_period=pay_period,
period_number=period_number,
client=client,
json_body=json_body,
ordinal=ordinal,
send_payslip_emails=send_payslip_emails,
payslip_release_type=payslip_release_type,
payslip_scheduled_date_time=payslip_scheduled_date_time,

    )).parsed

