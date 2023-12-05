import datetime
from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.contract_reapply_dps_notice_response import ContractReapplyDpsNoticeResponse
from ...types import UNSET, Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    applied_from_date: datetime.datetime,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/dps/reapply".format(client.base_url, employerId=employer_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_applied_from_date = applied_from_date.isoformat()

    params["appliedFromDate"] = json_applied_from_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ContractReapplyDpsNoticeResponse]:
    if response.status_code == 200:
        response_200 = ContractReapplyDpsNoticeResponse.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[ContractReapplyDpsNoticeResponse]:
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
    applied_from_date: datetime.datetime,
) -> Response[ContractReapplyDpsNoticeResponse]:
    """Reapply DpsNotices

     From a specified date onwards, reapply DpsNotices

    Args:
        employer_id (str):
        applied_from_date (datetime.datetime):

    Returns:
        Response[ContractReapplyDpsNoticeResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        applied_from_date=applied_from_date,
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
    applied_from_date: datetime.datetime,
) -> Optional[ContractReapplyDpsNoticeResponse]:
    """Reapply DpsNotices

     From a specified date onwards, reapply DpsNotices

    Args:
        employer_id (str):
        applied_from_date (datetime.datetime):

    Returns:
        Response[ContractReapplyDpsNoticeResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        applied_from_date=applied_from_date,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    applied_from_date: datetime.datetime,
) -> Response[ContractReapplyDpsNoticeResponse]:
    """Reapply DpsNotices

     From a specified date onwards, reapply DpsNotices

    Args:
        employer_id (str):
        applied_from_date (datetime.datetime):

    Returns:
        Response[ContractReapplyDpsNoticeResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        applied_from_date=applied_from_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    applied_from_date: datetime.datetime,
) -> Optional[ContractReapplyDpsNoticeResponse]:
    """Reapply DpsNotices

     From a specified date onwards, reapply DpsNotices

    Args:
        employer_id (str):
        applied_from_date (datetime.datetime):

    Returns:
        Response[ContractReapplyDpsNoticeResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            applied_from_date=applied_from_date,
        )
    ).parsed
