from typing import Any, Dict

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_options import PayOptions
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: PayOptions,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/payoptions".format(client.base_url, employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
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
    *,
    client: Client,
    json_body: PayOptions,
) -> Response[Any]:
    """Apply PayOptions

     Overwrite the PayOptions for all employees with the values provided.
    Currently only the following fields are updated: period, payAmount, basis, payamountMultiplier,
    nationalMinimumWage and regularPaylines.

    Args:
        employer_id (str):
        json_body (PayOptions): This object forms the basis of the Employees payment.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    *,
    client: Client,
    json_body: PayOptions,
) -> Response[Any]:
    """Apply PayOptions

     Overwrite the PayOptions for all employees with the values provided.
    Currently only the following fields are updated: period, payAmount, basis, payamountMultiplier,
    nationalMinimumWage and regularPaylines.

    Args:
        employer_id (str):
        json_body (PayOptions): This object forms the basis of the Employees payment.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
