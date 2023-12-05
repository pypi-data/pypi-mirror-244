from typing import Any, Dict

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.nic_summary import NicSummary
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: NicSummary,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/openingBalances/nic/{taxYear}".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, taxYear=tax_year
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: NicSummary,
) -> Response[Any]:
    """Create NicSummary

     Creates a NicSummary for for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (NicSummary):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: NicSummary,
) -> Response[Any]:
    """Create NicSummary

     Creates a NicSummary for for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (NicSummary):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
