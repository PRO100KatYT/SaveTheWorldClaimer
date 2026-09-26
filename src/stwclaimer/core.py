from api import EpicAPI, AuthAPI
from config import ConfigManager
from assets import Assets


class Context:
    def __init__(self):
        self.epic = EpicAPI()
        self.auth = AuthAPI(self.epic)
        self.cfg = ConfigManager()
        self.ast = Assets(
            self.cfg.global_config["ui_language"],
            self.cfg.global_config["items_language"],
        )
        self.cfg.reload_strings = self.ast.reload
