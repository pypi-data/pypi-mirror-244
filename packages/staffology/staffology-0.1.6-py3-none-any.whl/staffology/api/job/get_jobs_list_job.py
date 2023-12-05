from typing import Any, Dict, List, Optional, Union, cast

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_job_response import ContractJobResponse
from ...models.job_type import JobType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    job_type: Union[Unset, None, JobType] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/jobs".format(client.base_url, employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_job_type: Union[Unset, None, str] = UNSET
    if not isinstance(job_type, Unset):
        json_job_type = job_type.value if job_type else None

    params["jobType"] = json_job_type

    params["pageNum"] = page_num

    params["pageSize"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[ContractJobResponse]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ContractJobResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[ContractJobResponse]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    job_type: Union[Unset, None, JobType] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List[ContractJobResponse]]]:
    """List Jobs

     Returns a list of Jobs for an Employer for a given user with pagination

    Args:
        employer_id (str):
        job_type (Union[Unset, None, JobType]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[ContractJobResponse]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        job_type=job_type,
        page_num=page_num,
        page_size=page_size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    *,
    client: Client,
    job_type: Union[Unset, None, JobType] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List[ContractJobResponse]]]:
    """List Jobs

     Returns a list of Jobs for an Employer for a given user with pagination

    Args:
        employer_id (str):
        job_type (Union[Unset, None, JobType]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[ContractJobResponse]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        job_type=job_type,
        page_num=page_num,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    job_type: Union[Unset, None, JobType] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List[ContractJobResponse]]]:
    """List Jobs

     Returns a list of Jobs for an Employer for a given user with pagination

    Args:
        employer_id (str):
        job_type (Union[Unset, None, JobType]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[ContractJobResponse]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        job_type=job_type,
        page_num=page_num,
        page_size=page_size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    job_type: Union[Unset, None, JobType] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List[ContractJobResponse]]]:
    """List Jobs

     Returns a list of Jobs for an Employer for a given user with pagination

    Args:
        employer_id (str):
        job_type (Union[Unset, None, JobType]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[ContractJobResponse]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            job_type=job_type,
            page_num=page_num,
            page_size=page_size,
        )
    ).parsed
