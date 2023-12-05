from typing import Any, Dict, Optional, Union

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.exb import Exb
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    force: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/exb/{taxYear}/{id}/submit".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Exb]:
    if response.status_code == 200:
        response_200 = Exb.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Exb]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    force: Union[Unset, None, bool] = False,
) -> Response[Exb]:
    """Submit EXB

     Submits an existing Expenses And Benefits submission to HMRC.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        force (Union[Unset, None, bool]):

    Returns:
        Response[Exb]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        force=force,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    force: Union[Unset, None, bool] = False,
) -> Optional[Exb]:
    """Submit EXB

     Submits an existing Expenses And Benefits submission to HMRC.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        force (Union[Unset, None, bool]):

    Returns:
        Response[Exb]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    force: Union[Unset, None, bool] = False,
) -> Response[Exb]:
    """Submit EXB

     Submits an existing Expenses And Benefits submission to HMRC.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        force (Union[Unset, None, bool]):

    Returns:
        Response[Exb]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        force=force,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    force: Union[Unset, None, bool] = False,
) -> Optional[Exb]:
    """Submit EXB

     Submits an existing Expenses And Benefits submission to HMRC.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        force (Union[Unset, None, bool]):

    Returns:
        Response[Exb]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            id=id,
            client=client,
            force=force,
        )
    ).parsed
