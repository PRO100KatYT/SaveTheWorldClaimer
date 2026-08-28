import httpx
import asyncio


async def get_access_token(auth_code: str) -> dict:
    req_headers = {
        "Authorization": "basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
    }

    json_body = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers=req_headers,
            data=json_body,
        )
        return response.json()


async def get_device_auth(access_token: str, account_id: str) -> dict:
    req_headers = {"Authorization": f"bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth",
            headers=req_headers,
            data={},
        )
        return response.json()
