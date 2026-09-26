import assets
import pathlib

ASSETS_BASE_PATH = pathlib.Path(__file__).parent / "jsons" / "assets"

DATA_FILE_PATH = ASSETS_BASE_PATH / "data.json"
INTERFACE_BASE_PATH = ASSETS_BASE_PATH / "locales" / "interface"
ITEMS_BASE_PATH = ASSETS_BASE_PATH / "locales" / "items"


def test_init():
    ast = assets.Assets(
        "en", "pl", DATA_FILE_PATH, INTERFACE_BASE_PATH, ITEMS_BASE_PATH
    )

    assert "main.login.success" in ast.interface
    assert ast.interface["main.login.success"] == "Logged in successfully"

    assert "Items" in ast.items
    assert "quest:daily_huskextermination_anyhero" in ast.items["Items"]
    assert (
        ast.items["Items"]["quest:daily_huskextermination_anyhero"]
        == "Eksterminacja pustaków (dowolny bohater)"
    )


def test_reload():
    ast = assets.Assets(
        "en", "pl", DATA_FILE_PATH, INTERFACE_BASE_PATH, ITEMS_BASE_PATH
    )

    ast.reload("pl", "de", INTERFACE_BASE_PATH, ITEMS_BASE_PATH)

    assert "main.login.success" in ast.interface
    assert ast.interface["main.login.success"] == "Zalogowano pomyślnie"

    assert "Items" in ast.items
    assert "quest:daily_huskextermination_anyhero" in ast.items["Items"]
    assert (
        ast.items["Items"]["quest:daily_huskextermination_anyhero"]
        == "Hüllenausrottung (Beliebiger Held)"
    )
