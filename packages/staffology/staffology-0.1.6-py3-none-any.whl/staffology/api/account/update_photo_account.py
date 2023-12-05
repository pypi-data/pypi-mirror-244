from typing import Any, Dict, Optional

import httpx
from staffology.propagate_exceptions import raise_staffology_exception

from ...client import Client
from ...models.update_photo_account_multipart_data import UpdatePhotoAccountMultipartData
from ...models.user import User
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    multipart_data: UpdatePhotoAccountMultipartData,
) -> Dict[str, Any]:
    url = "{}/account/photo".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[User]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    return raise_staffology_exception(response)


def _build_response(*, response: httpx.Response) -> Response[User]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: UpdatePhotoAccountMultipartData,
) -> Response[User]:
    """Update Photo

     Submit an image here and we'll upload it, resize it to 200px squared and set it as the image for
    your account.

    Args:
        multipart_data (UpdatePhotoAccountMultipartData):

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: UpdatePhotoAccountMultipartData,
) -> Optional[User]:
    """Update Photo

     Submit an image here and we'll upload it, resize it to 200px squared and set it as the image for
    your account.

    Args:
        multipart_data (UpdatePhotoAccountMultipartData):

    Returns:
        Response[User]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: UpdatePhotoAccountMultipartData,
) -> Response[User]:
    """Update Photo

     Submit an image here and we'll upload it, resize it to 200px squared and set it as the image for
    your account.

    Args:
        multipart_data (UpdatePhotoAccountMultipartData):

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: UpdatePhotoAccountMultipartData,
) -> Optional[User]:
    """Update Photo

     Submit an image here and we'll upload it, resize it to 200px squared and set it as the image for
    your account.

    Args:
        multipart_data (UpdatePhotoAccountMultipartData):

    Returns:
        Response[User]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
