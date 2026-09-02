import httpx
import asyncio


class EpicAPI:
    def __init__(self):
        self.session = httpx.AsyncClient()

    def set_access_token(self, access_token: str) -> None:
        self.session.headers.update({"Authorization": f"bearer {access_token}"})


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

        response = await self.epic.session.post(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers=req_headers,
            data=json_body,
        )
        return response.json()

    async def get_device_auth(self, account_id: str) -> dict:
        response = await self.epic.session.post(
            f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth",
            data={},
        )
        return response.json()
