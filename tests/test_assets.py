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

    assert "main.login.success" in ast.ui
    assert ast.ui["main.login.success"] == "Logged in successfully"

    assert "items" in ast.items
    assert "quest:daily_huskextermination_anyhero" in ast.items["items"]
    assert (
        ast.items["items"]["quest:daily_huskextermination_anyhero"]
        == "Eksterminacja pustaków (dowolny bohater)"
    )


def test_load_data():
    ast = assets.Assets(
        "pl", "de", DATA_FILE_PATH, INTERFACE_BASE_PATH, ITEMS_BASE_PATH
    )
    ast.load_data(DATA_FILE_PATH)

    assert "items" in ast.data
    assert "hero:hid_commando_gunheadshothw_vr_t01" in ast.data["items"]

    item = ast.data["items"]["hero:hid_commando_gunheadshothw_vr_t01"]
    assert item["rarity"] == "epic"
    assert item["type"] == "hero"


def test_load_ui():
    ast = assets.Assets(
        "pl", "de", DATA_FILE_PATH, INTERFACE_BASE_PATH, ITEMS_BASE_PATH
    )
    ast.load_ui("pl", INTERFACE_BASE_PATH)

    assert "main.login.success" in ast.ui
    assert ast.ui["main.login.success"] == "Zalogowano pomyślnie"


def test_load_items():
    ast = assets.Assets(
        "pl", "de", DATA_FILE_PATH, INTERFACE_BASE_PATH, ITEMS_BASE_PATH
    )
    ast.load_items("de", ITEMS_BASE_PATH)

    assert "items" in ast.items
    assert "quest:daily_huskextermination_anyhero" in ast.items["items"]
    assert (
        ast.items["items"]["quest:daily_huskextermination_anyhero"]
        == "Hüllenausrottung (Beliebiger Held)"
    )
