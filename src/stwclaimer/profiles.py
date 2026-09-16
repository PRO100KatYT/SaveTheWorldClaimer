import api


class ProfileManager:
    def __init__(self, mcp_api: api.McpAPI):
        self.mcp = mcp_api
        self.cache = {}

    def process_profile_changes(self, profile_changes: list, profile_id: str) -> None:
        for entry in profile_changes:
            match entry["changeType"]:
                case "itemAdded":
                    return

                case "itemRemoved":
                    return

                case "itemAttrChanged":
                    return

                case "itemQuantityChanged":
                    return

                case "statModified":
                    return

                case "fullProfileUpdate":
                    self.cache[profile_id] = entry["profile"]

                case _:
                    return

    async def base_request(
        self, operation: str, profile_id: str, json_body: dict = {}
    ) -> dict:
        res = await self.mcp.client_request(operation, profile_id, json_body)

        profile_updates = {}

        if "multiUpdate" in res:
            for entry in res["multiUpdate"]:
                profile_updates[entry["profileId"]] = entry
            del res["multiUpdate"]

        profile_updates[res["profileId"]] = res

        for res_profile_id in profile_updates:
            self.process_profile_changes(
                profile_updates[res_profile_id]["profileChanges"], res_profile_id
            )

        return profile_updates

    async def query_profile(self, profile_id: str) -> dict:
        return await self.base_request("QueryProfile", profile_id)
