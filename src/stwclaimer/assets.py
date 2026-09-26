import utils
from pathlib import Path
import json

ASSETS_BASE_PATH = utils.base_path(False) / "assets"

DATA_FILE_PATH = ASSETS_BASE_PATH / "data.json"
INTERFACE_BASE_PATH = ASSETS_BASE_PATH / "locales" / "interface"
ITEMS_BASE_PATH = ASSETS_BASE_PATH / "locales" / "items"


class Assets:
    def __init__(
        self,
        ui_language: str,
        items_language: str,
        data_file_path: Path = DATA_FILE_PATH,
        ui_path: Path = INTERFACE_BASE_PATH,
        items_path: Path = ITEMS_BASE_PATH,
    ):
        self.interface = {}
        self.items = {}

        self.reload(ui_language, items_language, ui_path, items_path)

        self.data = {}
        self.load_data(data_file_path)

    def load_data(self, data_file_path: Path = DATA_FILE_PATH) -> None:
        with open(data_file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def reload(
        self,
        ui_language: str,
        items_language: str,
        ui_path: Path = INTERFACE_BASE_PATH,
        items_path: Path = ITEMS_BASE_PATH,
    ) -> None:
        with open(ui_path / f"{ui_language}.json", "r", encoding="utf-8") as file:
            self.interface = json.load(file)
        with open(items_path / f"{items_language}.json", "r", encoding="utf-8") as file:
            self.items = json.load(file)

    def get_ui_str(self, key: str) -> str:
        return self.interface.get(key, key)

    def get_type_str(self, item_type_lower: str) -> str:
        return self.items["types"].get(item_type_lower, item_type_lower)

    def get_rarity_str(self, rarity_lower: str) -> str:
        return self.items["rarities"].get(rarity_lower, rarity_lower)

    def get_item_str(self, template_id_lower: str) -> str:
        return self.items["items"].get(template_id_lower, template_id_lower)

    def get_objective_str(self, objective_lower: str) -> str:
        return self.items["objectives"].get(objective_lower, objective_lower)
