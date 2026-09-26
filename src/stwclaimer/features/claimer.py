import auth
import api
import core
import profiles
from features import daily_quests


async def loop(ctx: core.Context) -> None:
    auth_json = auth.read_auth()
    for account_id in auth_json:
        display_name = auth_json[account_id]["display_name"]
        print(
            ctx.ast.get_ui_str("claimer.loop.loggingin").format(display_name), end=" "
        )

        await auth.login(ctx.auth, account_id, auth_json)

        print(ctx.ast.get_ui_str("claimer.loop.success"))

        mcp = api.McpAPI(account_id, ctx.epic)
        manager = profiles.ProfileManager(mcp)

        await daily_quests.main(ctx, manager)
