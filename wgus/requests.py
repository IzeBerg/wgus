from typing import Dict

import aiohttp
from yarl import URL


async def request(method: str, host: str, path: str, query: Dict[str, str]) -> str:
    async with aiohttp.request(
        method, URL.build(scheme="https", host=host, path=path, query=query)
    ) as req:
        req.raise_for_status()
        return await req.text()


async def get(host: str, path: str, query: Dict[str, str]) -> str:
    return await request("GET", host, path, query)
