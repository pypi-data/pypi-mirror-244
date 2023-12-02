import os
from typing import Optional
import json


def call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None):
    import requests
    if workspace_api_key is None:
        workspace_api_key = os.environ.get("INFERLESS_API_KEY")
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {workspace_api_key}"}
    if data is None:
        data = {}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to call {url} with status code {response.status_code} and response {response.text}")
    return response.json()


async def async_call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None):
    import aiohttp
    if workspace_api_key is None:
        workspace_api_key = os.environ.get("INFERLESS_API_KEY")

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {workspace_api_key}"}
    if data is None:
        data = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=json.dumps(data)) as response:
            if response.status != 200:
                raise Exception(
                    f"Failed to call {url} with status code {response.status} and response {await response.text()}")
            return await response.json()
