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

USER_CONFIG_DATA = {
    "llama_loot_recycling": {
        "recycle_weapons": {
            "display_name": "config.recycle_weapons.display_name",
            "description": "config.recycle_weapons.description",
            "type": str,
            "valid_values": ["off", "common", "uncommon", "rare", "epic"],
            "default": "rare",
        },
        "recycle_traps": {
            "display_name": "config.recycle_traps.display_name",
            "description": "config.recycle_traps.description",
            "type": str,
            "valid_values": ["off", "common", "uncommon", "rare", "epic"],
            "default": "rare",
        },
        "retire_survivors": {
            "display_name": "config.retire_survivors.display_name",
            "description": "config.retire_survivors.description",
            "type": str,
            "valid_values": ["off", "common", "uncommon", "rare", "epic"],
            "default": "epic",
        },
        "retire_defenders": {
            "display_name": "config.retire_defenders.display_name",
            "description": "config.retire_defenders.description",
            "type": str,
            "valid_values": ["off", "common", "uncommon", "rare", "epic"],
            "default": "epic",
        },
        "retire_heroes": {
            "display_name": "config.retire_heroes.display_name",
            "description": "config.retire_heroes.description",
            "type": str,
            "valid_values": ["off", "common", "uncommon", "rare", "epic"],
            "default": "rare",
        },
    },
}


class ConfigManager:
    def __init__(self):
        self.global_config = self.get_default_global_config()
        self.user_config = defaultdict(dict)
        self._listeners = defaultdict(list)

        self.load_global_config()
        self.load_user_config()

    def get_default_global_config(self) -> dict:
        global_config = {}

        for option in GLOBAL_CONFIG_DATA:
            global_config[option] = GLOBAL_CONFIG_DATA[option]["default"]

        return global_config

    def get_user_config(self, account_id: str) -> dict:
        def crawl(data_part: dict, config_part: dict) -> None:
            for key in data_part:
                if "type" in data_part[key]:
                    if key not in config_part:
                        config_part[key] = data_part[key]["default"]
                else:
                    if key not in config_part:
                        config_part[key] = {}
                    crawl(data_part[key], config_part[key])

        crawl(USER_CONFIG_DATA, self.user_config[account_id])

        self.save_user_config()

        return self.user_config[account_id]

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

    def set_user_value(self, account_id: str, path: list, value) -> None:
        config_part = self.user_config[account_id]

        for i in range(len(path) - 1):
            config_part = config_part[path[i]]

        config_part[path[-1]] = value

        self.save_user_config()
