import api
import config


class Context:
    def __init__(self):
        self.epic = api.EpicAPI()
        self.auth = api.AuthAPI(self.epic)
        self.cfg = config.ConfigManager()
