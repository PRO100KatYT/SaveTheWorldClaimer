import utils
from pathlib import Path
import json

GLOBAL_CONFIG_PATH: Path = utils.base_path(False) / "config.json"
USER_CONFIG_PATH: Path = utils.base_path(False) / "user_config.json"


class ConfigManager:
    def __init__(self):
        self.global_config = {
            "language": "en",
            "items_language": "en",
            "open_free_llamas": True,
            "show_date_time": True,
            "discord_webhook_url": "",
            "check_for_updates": True,
        }
        self.user_config = {}

        self.load_global_config()
        self.load_user_config()

    def save_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> bool:
        try:
            with open(path, "w") as file:
                json.dump(self.global_config, file, indent=2, ensure_ascii=False)
                return True
        except PermissionError:
            return False

    def save_user_config(self, path: Path = USER_CONFIG_PATH) -> bool:
        try:
            with open(path, "w") as file:
                json.dump(self.user_config, file, indent=2, ensure_ascii=False)
                return True
        except PermissionError:
            return False

    def load_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> None:
        try:
            with open(path, "r") as file:
                self.global_config.update(json.load(file))
        except FileNotFoundError:
            self.save_global_config(path)
        except json.JSONDecodeError:
            path.unlink()
            self.save_global_config(path)

    def load_user_config(self, path: Path = USER_CONFIG_PATH) -> None:
        try:
            with open(path, "r") as file:
                self.user_config.update(json.load(file))
        except FileNotFoundError:
            self.save_user_config(path)
        except json.JSONDecodeError:
            path.unlink()
            self.save_user_config(path)
