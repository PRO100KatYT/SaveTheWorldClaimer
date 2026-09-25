import auth
import api
import core
import profiles
from features import daily_quests


async def loop(context: core.Context) -> None:
    auth_json = auth.read_auth()
    for account_id in auth_json:
        display_name = auth_json[account_id]["display_name"]
        print(f"\nLogging in as {display_name}...", end=" ")

        await auth.login(context.auth, account_id, auth_json)

        print(f"Done!\n")

        mcp = api.McpAPI(account_id, context.epic)
        manager = profiles.ProfileManager(mcp)

        await daily_quests.main(manager)
