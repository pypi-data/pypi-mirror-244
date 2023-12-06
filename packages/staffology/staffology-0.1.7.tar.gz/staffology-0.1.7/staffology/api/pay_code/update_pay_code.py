from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.pay_code import PayCode
from ...types import Response


def _get_kwargs(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: PayCode,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/paycodes/{code}".format(client.base_url, employerId=employer_id, code=code)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PayCode]]:
    if response.status_code == 200:
        response_200 = PayCode.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PayCode]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: PayCode,
) -> Response[Union[Any, PayCode]]:
    """Update PayCode (deprecated)

     Updates the details of an existing PayCode.
    Use the other Update endpoint that supports non-alphanumeric characters for a pay code

    Args:
        employer_id (str):
        code (str):
        json_body (PayCode): Each PayLine has a Code. The Code will match the Code property of a
            PayCode.
            The PayCode that is used determines how the amount is treated with regards to tax, NI and
            pensions

    Returns:
        Response[Union[Any, PayCode]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
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
    code: str,
    *,
    client: Client,
    json_body: PayCode,
) -> Optional[Union[Any, PayCode]]:
    """Update PayCode (deprecated)

     Updates the details of an existing PayCode.
    Use the other Update endpoint that supports non-alphanumeric characters for a pay code

    Args:
        employer_id (str):
        code (str):
        json_body (PayCode): Each PayLine has a Code. The Code will match the Code property of a
            PayCode.
            The PayCode that is used determines how the amount is treated with regards to tax, NI and
            pensions

    Returns:
        Response[Union[Any, PayCode]]
    """

    return sync_detailed(
        employer_id=employer_id,
        code=code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: PayCode,
) -> Response[Union[Any, PayCode]]:
    """Update PayCode (deprecated)

     Updates the details of an existing PayCode.
    Use the other Update endpoint that supports non-alphanumeric characters for a pay code

    Args:
        employer_id (str):
        code (str):
        json_body (PayCode): Each PayLine has a Code. The Code will match the Code property of a
            PayCode.
            The PayCode that is used determines how the amount is treated with regards to tax, NI and
            pensions

    Returns:
        Response[Union[Any, PayCode]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: PayCode,
) -> Optional[Union[Any, PayCode]]:
    """Update PayCode (deprecated)

     Updates the details of an existing PayCode.
    Use the other Update endpoint that supports non-alphanumeric characters for a pay code

    Args:
        employer_id (str):
        code (str):
        json_body (PayCode): Each PayLine has a Code. The Code will match the Code property of a
            PayCode.
            The PayCode that is used determines how the amount is treated with regards to tax, NI and
            pensions

    Returns:
        Response[Union[Any, PayCode]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            code=code,
            client=client,
            json_body=json_body,
        )
    ).parsed
