import api


class ProfileManager:
    def __init__(self, mcp_api: api.McpAPI):
        self.mcp = mcp_api
        self.cache = {}
