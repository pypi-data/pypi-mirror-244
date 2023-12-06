from io import BytesIO
from typing import Any, Dict, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...types import File, Response


def _get_kwargs(
    employer_id: str,
    job_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/jobs/{jobId}/document".format(
        client.base_url, employerId=employer_id, jobId=job_id
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, File]]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, File]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    job_id: str,
    *,
    client: Client,
) -> Response[Union[Any, File]]:
    """Get Job file

     Returns the file generated for a successfully completed Job of type Report as a string representing
    a filestream.

    Args:
        employer_id (str):
        job_id (str):

    Returns:
        Response[Union[Any, File]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        job_id=job_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    job_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, File]]:
    """Get Job file

     Returns the file generated for a successfully completed Job of type Report as a string representing
    a filestream.

    Args:
        employer_id (str):
        job_id (str):

    Returns:
        Response[Union[Any, File]]
    """

    return sync_detailed(
        employer_id=employer_id,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    job_id: str,
    *,
    client: Client,
) -> Response[Union[Any, File]]:
    """Get Job file

     Returns the file generated for a successfully completed Job of type Report as a string representing
    a filestream.

    Args:
        employer_id (str):
        job_id (str):

    Returns:
        Response[Union[Any, File]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        job_id=job_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    job_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, File]]:
    """Get Job file

     Returns the file generated for a successfully completed Job of type Report as a string representing
    a filestream.

    Args:
        employer_id (str):
        job_id (str):

    Returns:
        Response[Union[Any, File]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            job_id=job_id,
            client=client,
        )
    ).parsed
