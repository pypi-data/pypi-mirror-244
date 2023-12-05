from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.eps import Eps
from ...models.exb import Exb
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: Exb,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/exb/{taxYear}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year
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


def _parse_response(*, response: httpx.Response) -> Optional[Eps]:
    if response.status_code == 201:
        response_201 = Eps.from_dict(response.json())

        return response_201
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Eps]:
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
    json_body: Exb,
) -> Response[Eps]:
    """Create EXB

     Creates a new Expenses And Benefits submission

    Args:
        employer_id (str):
        tax_year (TaxYear):
        json_body (Exb):

    Returns:
        Response[Eps]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
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
    json_body: Exb,
) -> Optional[Eps]:
    """Create EXB

     Creates a new Expenses And Benefits submission

    Args:
        employer_id (str):
        tax_year (TaxYear):
        json_body (Exb):

    Returns:
        Response[Eps]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: Exb,
) -> Response[Eps]:
    """Create EXB

     Creates a new Expenses And Benefits submission

    Args:
        employer_id (str):
        tax_year (TaxYear):
        json_body (Exb):

    Returns:
        Response[Eps]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: Exb,
) -> Optional[Eps]:
    """Create EXB

     Creates a new Expenses And Benefits submission

    Args:
        employer_id (str):
        tax_year (TaxYear):
        json_body (Exb):

    Returns:
        Response[Eps]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            client=client,
            json_body=json_body,
        )
    ).parsed
