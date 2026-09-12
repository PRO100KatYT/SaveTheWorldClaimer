import auth
import api
import profiles


async def loop(epic_api: api.EpicAPI, auth_api: api.AuthAPI) -> None:
    auth_json = auth.read_auth()
    for account_id in auth_json:
        display_name = auth_json[account_id]["display_name"]
        print(f"\nLogging in as {display_name}... ", end="")

        await auth.login(auth_api, account_id, auth_json)

        print(f"Done!\n")

        mcp = api.McpAPI(account_id, epic_api)
        manager = profiles.ProfileManager(mcp)
