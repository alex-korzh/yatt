import asyncio
import json
import logging

import httpx
from pydantic import BaseModel

from app.config import config

logger = logging.getLogger(__name__)

class Auth0DeviceInfo(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    interval: int



async def auth0_request_device_code() -> Auth0DeviceInfo:
    auth0_code_url = config.auth0.base_url + "device/code"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": config.auth0.client_id,
        "scope": "sub",
        "audience": config.auth0.api_id,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(auth0_code_url, headers=headers, data=data)
    return Auth0DeviceInfo.model_validate_json(resp.text)

async def auth0_request_token(device_code: str) -> dict:
    auth0_token_url = config.auth0.base_url + "token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": config.auth0.client_id,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(auth0_token_url, headers=headers, data=data)
    return json.loads(resp.text)


async def authenticate():
    device_info: Auth0DeviceInfo = await auth0_request_device_code()
    print(device_info)
    while "error" in (maybe_token := await auth0_request_token(device_info.device_code)):
        logger.debug("Polling for auth token...")
        match maybe_token["error"]:
            case "authorization_pending":
                await asyncio.sleep(device_info.interval)
            case "slow_down":
                device_info.interval += 1
                await asyncio.sleep(device_info.interval)
            case _:
                logger.debug(f"Error: {maybe_token['error_description']}")
    print(maybe_token)
    return maybe_token["access_token"]



if __name__ == "__main__":
    asyncio.run(authenticate())