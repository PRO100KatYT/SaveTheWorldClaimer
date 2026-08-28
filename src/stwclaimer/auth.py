import utils
from pathlib import Path
import json
import api

AUTH_PATH: Path = utils.base_path(False) / "auth.json"
AUTH_CODE_LINK: str = (
    "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D3f69e56c7649492c8cc29f1af08a8a12%2526responseType%253Dcode"
)


def save_auth(auth_json: list) -> None:
    try:
        with open(AUTH_PATH, "w") as file:
            json.dump(auth_json, file, indent=2, ensure_ascii=False)
            return True
    except PermissionError:
        return None


def read_auth() -> list | None:
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

