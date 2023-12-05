from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.eps_apprenticeship_levy import EpsApprenticeshipLevy
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/eps/{taxYear}/{taxMonth}/apprenticeshipLevytodate".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, taxMonth=tax_month
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


def _parse_response(*, response: httpx.Response) -> Optional[EpsApprenticeshipLevy]:
    if response.status_code == 200:
        response_200 = EpsApprenticeshipLevy.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[EpsApprenticeshipLevy]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Response[EpsApprenticeshipLevy]:
    """Apprenticeship Levy

     Get all Apprenticeship Levy (SMP, etc) for a given tax year, up to the given tax month, and if the
    'Linked EPS'
    is enabled by the employer, apprenticeship levy as well as the apprenticeship levy for any employers
    with 'Linked EPS' enabled and with the same PAYE scheme
    is returned as a sum.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[EpsApprenticeshipLevy]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
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
    tax_month: int,
    *,
    client: Client,
) -> Optional[EpsApprenticeshipLevy]:
    """Apprenticeship Levy

     Get all Apprenticeship Levy (SMP, etc) for a given tax year, up to the given tax month, and if the
    'Linked EPS'
    is enabled by the employer, apprenticeship levy as well as the apprenticeship levy for any employers
    with 'Linked EPS' enabled and with the same PAYE scheme
    is returned as a sum.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[EpsApprenticeshipLevy]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Response[EpsApprenticeshipLevy]:
    """Apprenticeship Levy

     Get all Apprenticeship Levy (SMP, etc) for a given tax year, up to the given tax month, and if the
    'Linked EPS'
    is enabled by the employer, apprenticeship levy as well as the apprenticeship levy for any employers
    with 'Linked EPS' enabled and with the same PAYE scheme
    is returned as a sum.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[EpsApprenticeshipLevy]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Optional[EpsApprenticeshipLevy]:
    """Apprenticeship Levy

     Get all Apprenticeship Levy (SMP, etc) for a given tax year, up to the given tax month, and if the
    'Linked EPS'
    is enabled by the employer, apprenticeship levy as well as the apprenticeship levy for any employers
    with 'Linked EPS' enabled and with the same PAYE scheme
    is returned as a sum.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[EpsApprenticeshipLevy]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            tax_month=tax_month,
            client=client,
        )
    ).parsed
