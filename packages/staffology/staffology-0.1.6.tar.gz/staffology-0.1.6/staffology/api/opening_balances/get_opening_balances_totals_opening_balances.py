from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.opening_balances_totals import OpeningBalancesTotals
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/openingbalances/{taxYear}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, OpeningBalancesTotals]]:
    if response.status_code == 200:
        response_200 = OpeningBalancesTotals.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, OpeningBalancesTotals]]:
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
) -> Response[Union[Any, OpeningBalancesTotals]]:
    """Totals of employee opening balances for a tax year

     Totals of Employee Opening Balances in the specified TaxYear

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Union[Any, OpeningBalancesTotals]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    tax_year: TaxYear,
    *,
    client: Client,
) -> Optional[Union[Any, OpeningBalancesTotals]]:
    """Totals of employee opening balances for a tax year

     Totals of Employee Opening Balances in the specified TaxYear

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Union[Any, OpeningBalancesTotals]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Response[Union[Any, OpeningBalancesTotals]]:
    """Totals of employee opening balances for a tax year

     Totals of Employee Opening Balances in the specified TaxYear

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Union[Any, OpeningBalancesTotals]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Optional[Union[Any, OpeningBalancesTotals]]:
    """Totals of employee opening balances for a tax year

     Totals of Employee Opening Balances in the specified TaxYear

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Union[Any, OpeningBalancesTotals]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            client=client,
        )
    ).parsed
