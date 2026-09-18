import auth
import pathlib

AUTH_PATH = pathlib.Path(__file__).parent / "auth.json"


def test_save_and_read_auth():
    content = {
        "test_account_id": {
            "display_name": "Gry_Wojenne",
            "device_id": "test_device_id",
            "secret": "test_secret",
        }
    }

    assert auth.save_auth(content, AUTH_PATH)

    auth_json = auth.read_auth(AUTH_PATH)

    assert auth_json == content

    AUTH_PATH.unlink()


def test_read_non_json_auth_file():
    with open(AUTH_PATH, "w") as file:
        file.write("e")

    auth_json = auth.read_auth(AUTH_PATH)
    assert auth_json == {}

    AUTH_PATH.unlink()


def test_read_non_existing_auth_file():
    auth_json = auth.read_auth(AUTH_PATH)
    assert auth_json == {}

    AUTH_PATH.unlink()
