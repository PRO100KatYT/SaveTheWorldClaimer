import utils
from pathlib import Path
import json
from collections import defaultdict

GLOBAL_CONFIG_PATH: Path = utils.base_path(False) / "config.json"
USER_CONFIG_PATH: Path = utils.base_path(False) / "user_config.json"


GLOBAL_CONFIG_DATA = {
    "ui_language": {
        "display_name": "config.ui_language.display_name",
        "description": "config.ui_language.description",
        "type": str,
        "valid_values": ["en", "pl"],
        "default": "en",
    },
    "items_language": {
        "display_name": "config.items_language.display_name",
        "description": "config.items_language.description",
        "type": str,
        "valid_values": [
            "ar",
            "de",
            "en",
            "es-419",
            "es",
            "fr",
            "id",
            "it",
            "ja",
            "ko",
            "pl",
            "pt-BR",
            "ru",
            "th",
            "tr",
            "vi",
            "zh-Hans",
            "zh-Hant",
        ],
        "default": "en",
    },
    "open_free_llamas": {
        "display_name": "config.open_free_llamas.display_name",
        "description": "config.open_free_llamas.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
    "show_date_time": {
        "display_name": "config.show_date_time.display_name",
        "description": "config.show_date_time.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
    "discord_webhook_url": {
        "display_name": "config.discord_webhook_url.display_name",
        "description": "config.discord_webhook_url.description",
        "type": str,
        "valid_values": [],
        "default": "",
    },
    "check_for_updates": {
        "display_name": "config.check_for_updates.display_name",
        "description": "config.check_for_updates.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
}


class ConfigManager:
    def __init__(self):
        self.global_config = self.get_default_global_config()
        self.user_config = {}
        self._listeners = defaultdict(list)

        self.load_global_config()
        self.load_user_config()

    def get_default_global_config(self) -> dict:
        global_config = {}

        for option in GLOBAL_CONFIG_DATA:
            global_config[option] = GLOBAL_CONFIG_DATA[option]["default"]

        return global_config

    def save_config(self, path: Path, config: dict) -> bool:
        try:
            with open(path, "w") as file:
                json.dump(config, file, indent=2, ensure_ascii=False)
                return True
        except PermissionError:
            return False

    def save_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> bool:
        return self.save_config(path, self.global_config)

    def save_user_config(self, path: Path = USER_CONFIG_PATH) -> bool:
        return self.save_config(path, self.user_config)

    def load_config(self, path: Path, destination: dict, save_function) -> None:
        try:
            with open(path, "r") as file:
                destination.update(json.load(file))
        except FileNotFoundError:
            save_function(path)
        except json.JSONDecodeError:
            path.unlink()
            save_function(path)

    def load_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> None:
        self.load_config(path, self.global_config, self.save_global_config)

    def load_user_config(self, path: Path = USER_CONFIG_PATH) -> None:
        self.load_config(path, self.user_config, self.save_user_config)

    def add_listener(self, option: str, function) -> None:
        self._listeners[option].append(function)

    def notify_listeners(self, option: str) -> None:
        functions = self._listeners.get(option, [])

        for function in functions:
            function(self.global_config[option])

    def set_global_value(self, option: str, value) -> None:
        if self.global_config[option] == value:
            return

        self.global_config[option] = value
        self.save_global_config()
        self.notify_listeners(option)
