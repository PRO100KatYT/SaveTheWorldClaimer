import utils
from pathlib import Path
import json
from collections import defaultdict

GLOBAL_CONFIG_PATH: Path = utils.base_path(False) / "config.json"
USER_CONFIG_PATH: Path = utils.base_path(False) / "user_config.json"


class ConfigManager:
    def __init__(self):
        self.global_config = {
            "ui_language": "en",
            "items_language": "en",
            "open_free_llamas": True,
            "show_date_time": True,
            "display_colors": True,
            "discord_webhook_url": "",
            "check_for_updates": True,
        }
        self.user_config = {}
        self._listeners = defaultdict(list)

        self.load_global_config()
        self.load_user_config()

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
