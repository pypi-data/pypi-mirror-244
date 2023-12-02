from typing import Optional

import aiohttp
import async_timeout
from aiohttp import ClientConnectorError, ContentTypeError, JsonPayload
from fastapi import HTTPException, Response


async def make_request(
    url: str,
    method: str,
    headers: dict = None,
    query: Optional[dict] = None,
    data: str = None,
    json: JsonPayload = None,
    timeout: int = 60,
):
    async with async_timeout.timeout(delay=timeout):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(
                method=method, url=url, params=query, data=data, json=json
            ) as response:
                if response.status == 204:
                    response_json = Response(status_code=204)
                else:
                    response_json = await response.json()
                decoded_json = response_json
                return decoded_json, response.status, response.headers


async def request(url, method, headers=None, data=None, json=None, query=None):
    try:
        (x, y, z) = await make_request(
            url=url, method=method, headers=headers, data=data, json=json, query=query
        )
    except ClientConnectorError:
        raise HTTPException(status_code=503, detail="Service is unavailable.")
    except ContentTypeError:
        raise HTTPException(status_code=500, detail="Service error.")
    return x, y, z

