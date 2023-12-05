from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_run_entry import PayRunEntry
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    pension_unique_id: str,
    tax_year: TaxYear,
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/pension/{pensionUniqueId}/{taxYear}/pensionytd".format(
        client.base_url,employerId=employer_id,employeeId=employee_id,pensionUniqueId=pension_unique_id,taxYear=tax_year)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayRunEntry]:
    if response.status_code == 200:
        response_200 = PayRunEntry.from_dict(response.json())



        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[PayRunEntry]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    pension_unique_id: str,
    tax_year: TaxYear,
    *,
    client: Client,

) -> Response[PayRunEntry]:
    """Gets the last pay run entry with pension brought forward values for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        pension_unique_id (str):
        tax_year (TaxYear):

    Returns:
        Response[PayRunEntry]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
employee_id=employee_id,
pension_unique_id=pension_unique_id,
tax_year=tax_year,
client=client,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    employer_id: str,
    employee_id: str,
    pension_unique_id: str,
    tax_year: TaxYear,
    *,
    client: Client,

) -> Optional[PayRunEntry]:
    """Gets the last pay run entry with pension brought forward values for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        pension_unique_id (str):
        tax_year (TaxYear):

    Returns:
        Response[PayRunEntry]
    """


    return sync_detailed(
        employer_id=employer_id,
employee_id=employee_id,
pension_unique_id=pension_unique_id,
tax_year=tax_year,
client=client,

    ).parsed

async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    pension_unique_id: str,
    tax_year: TaxYear,
    *,
    client: Client,

) -> Response[PayRunEntry]:
    """Gets the last pay run entry with pension brought forward values for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        pension_unique_id (str):
        tax_year (TaxYear):

    Returns:
        Response[PayRunEntry]
    """


    kwargs = _get_kwargs(
        employer_id=employer_id,
employee_id=employee_id,
pension_unique_id=pension_unique_id,
tax_year=tax_year,
client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    employer_id: str,
    employee_id: str,
    pension_unique_id: str,
    tax_year: TaxYear,
    *,
    client: Client,

) -> Optional[PayRunEntry]:
    """Gets the last pay run entry with pension brought forward values for an employee.

    Args:
        employer_id (str):
        employee_id (str):
        pension_unique_id (str):
        tax_year (TaxYear):

    Returns:
        Response[PayRunEntry]
    """


    return (await asyncio_detailed(
        employer_id=employer_id,
employee_id=employee_id,
pension_unique_id=pension_unique_id,
tax_year=tax_year,
client=client,

    )).parsed

