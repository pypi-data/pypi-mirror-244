from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.report_response import ReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    exclude_employees_with_p11_d_email_sent: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/p11d".format(
        client.base_url,employerId=employer_id,taxYear=tax_year)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept



    

    params: Dict[str, Any] = {}
    params["excludeEmployeesWithP11dEmailSent"] = exclude_employees_with_p11_d_email_sent



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
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    exclude_employees_with_p11_d_email_sent: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[ReportResponse]:
    """All P11Ds For TaxYear

     Returns all P11Ds in a single PDF file for the TaxYear and Employer specified
    If you set the accept header to \"text/html\" then unlike other reports the html is NOT in the
    ```Content``` field.
    As there are multiple HTML documents they are encoded as a JSON array of strings in the ```Model```
    field.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        exclude_employees_with_p11_d_email_sent (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
client=client,
exclude_employees_with_p11_d_email_sent=exclude_employees_with_p11_d_email_sent,
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
    *,
    client: Client,
    exclude_employees_with_p11_d_email_sent: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ReportResponse]:
    """All P11Ds For TaxYear

     Returns all P11Ds in a single PDF file for the TaxYear and Employer specified
    If you set the accept header to \"text/html\" then unlike other reports the html is NOT in the
    ```Content``` field.
    As there are multiple HTML documents they are encoded as a JSON array of strings in the ```Model```
    field.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        exclude_employees_with_p11_d_email_sent (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    return sync_detailed(
        employer_id=employer_id,
tax_year=tax_year,
client=client,
exclude_employees_with_p11_d_email_sent=exclude_employees_with_p11_d_email_sent,
accept=accept,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    exclude_employees_with_p11_d_email_sent: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Response[ReportResponse]:
    """All P11Ds For TaxYear

     Returns all P11Ds in a single PDF file for the TaxYear and Employer specified
    If you set the accept header to \"text/html\" then unlike other reports the html is NOT in the
    ```Content``` field.
    As there are multiple HTML documents they are encoded as a JSON array of strings in the ```Model```
    field.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        exclude_employees_with_p11_d_email_sent (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
tax_year=tax_year,
client=client,
exclude_employees_with_p11_d_email_sent=exclude_employees_with_p11_d_email_sent,
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
    *,
    client: Client,
    exclude_employees_with_p11_d_email_sent: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,

) -> Optional[ReportResponse]:
    """All P11Ds For TaxYear

     Returns all P11Ds in a single PDF file for the TaxYear and Employer specified
    If you set the accept header to \"text/html\" then unlike other reports the html is NOT in the
    ```Content``` field.
    As there are multiple HTML documents they are encoded as a JSON array of strings in the ```Model```
    field.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        exclude_employees_with_p11_d_email_sent (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
tax_year=tax_year,
client=client,
exclude_employees_with_p11_d_email_sent=exclude_employees_with_p11_d_email_sent,
accept=accept,

    )).parsed

