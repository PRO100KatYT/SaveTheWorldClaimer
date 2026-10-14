import utils
from pathlib import Path
import json
from collections import defaultdict

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
        self.ui = {}
        self.load_ui(ui_language, ui_path)

        self.items = {}
        self.load_items(items_language, items_path)

        self.data = {}
        self.load_data(data_file_path)

    def load_data(self, data_file_path: Path = DATA_FILE_PATH) -> None:
        with open(data_file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def load_ui(self, ui_language: str, ui_path: Path = INTERFACE_BASE_PATH) -> None:
        with open(ui_path / f"{ui_language}.json", "r", encoding="utf-8") as file:
            self.ui = json.load(file)

    def load_items(
        self, items_language: str, items_path: Path = ITEMS_BASE_PATH
    ) -> None:
        with open(items_path / f"{items_language}.json", "r", encoding="utf-8") as file:
            self.items = json.load(file)

    def get_item_data(self, template_id_lower) -> dict:
        return self.data["items"].get(template_id_lower, defaultdict(str))

    def get_ui_str(self, key: str) -> str:
        return self.ui.get(key, key)

    def get_type_str(self, item_type_lower: str) -> str:
        return self.items["types"].get(item_type_lower, item_type_lower)

    def get_rarity_str(self, rarity_lower: str) -> str:
        return self.items["rarities"].get(rarity_lower, rarity_lower)

    def get_rarity_color(self, rarity_lower: str) -> str:
        return self.items["rarity_colors"].get(rarity_lower, "#ffffff")

    def get_item_str(self, template_id_lower: str) -> str:
        return self.items["items"].get(template_id_lower, template_id_lower)

    def get_objective_str(self, objective_lower: str) -> str:
        return self.items["objectives"].get(objective_lower, objective_lower)

    def get_plural_word(self, key: str, number: int) -> str:
        if number == 1:
            plural = "one"
        elif number % 10 in [2, 3, 4] and not (12 <= (number % 100) <= 14):
            plural = "few"
        else:
            plural = "many"

        word = self.ui["words"][key]
        return word.get(plural, word.get("other", key))
