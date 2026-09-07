import httpx
import asyncio
from json import JSONDecodeError


class EpicAPI:
    def __init__(self):
        self.session = httpx.AsyncClient()

    def set_access_token(self, access_token: str) -> None:
        self.session.headers.update({"Authorization": f"bearer {access_token}"})

    async def request(self, method: str, *args, **kwargs):
        try:
            req = await self.session.request(method, *args, **kwargs)
            res = req.json()
            if "errorMessage" in res:
                raise ValueError(res["errorMessage"])
            return res
        except JSONDecodeError:
            raise ValueError("Failed to decode json from response.")
        except httpx.RequestError:
            raise ValueError("Failed to communicate with Epic Games servers.")

    async def post(self, *args, **kwargs) -> dict:
        return await self.request("post", *args, **kwargs)

    async def get(self, *args, **kwargs) -> dict:
        return await self.request("get", *args, **kwargs)


class AuthAPI:
    def __init__(self, epic: EpicAPI):
        self.epic = epic

    async def get_access_token(self, auth_code: str) -> dict:
        req_headers = {
            "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
        }

        json_body = {
            "grant_type": "authorization_code",
            "code": auth_code,
        }

        response = await self.epic.post(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers=req_headers,
            data=json_body,
        )
        return response

    async def get_device_auth(self, account_id: str) -> dict:
        response = await self.epic.post(
            f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth",
            data={},
        )
        return response
