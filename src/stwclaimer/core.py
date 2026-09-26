from api import EpicAPI, AuthAPI
from config import ConfigManager
from assets import Assets


class Context:
    def __init__(self):
        self.epic = EpicAPI()
        self.auth = AuthAPI(self.epic)
        self.cfg = ConfigManager()
        self.ast = Assets()
