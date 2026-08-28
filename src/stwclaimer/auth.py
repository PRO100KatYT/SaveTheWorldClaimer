import utils
from pathlib import Path
import json
import api

AUTH_PATH: Path = utils.base_path(False) / "auth.json"
AUTH_CODE_LINK: str = (
    "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3f69e56c7649492c8cc29f1af08a8a12%2526responseType%253Dcode"
)


def save_auth(auth_json: list) -> bool:
    try:
        with open(AUTH_PATH, "w") as file:
            json.dump(auth_json, file, indent=2, ensure_ascii=False)
            return True
    except PermissionError:
        return False


def read_auth() -> list:
    try:
        with open(AUTH_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        save_auth([])
        return []
    except json.JSONDecodeError:
        AUTH_PATH.unlink()
        save_auth([])
        return []


async def add_account(auth_code: str) -> bool:
    req_token = await api.get_access_token(auth_code)
    access_token, account_id, display_name = [
        req_token["access_token"],
        req_token["account_id"],
        req_token["displayName"],
    ]

    req_device = await api.get_device_auth(access_token, account_id)
    device_id, secret = [req_device["deviceId"], req_device["secret"]]

    auth_json = read_auth()
    auth_json.append(
        {
            "display_name": display_name,
            "account_id": account_id,
            "device_id": device_id,
            "secret": secret,
        }
    )
    save_auth(auth_json)

    return True
