import auth
import api
import core
import profiles
from cli import daily_quests_cli, llamas_cli, utils_cli, junk_cleaner_cli, item_shop_cli


async def loop(ctx: core.Context) -> None:
    auth_json = auth.read_auth()

    ctx.log.toggle_webhooks(True)
    ctx.log.message()

    for account_id in auth_json:
        await utils_cli.login_with_printing(ctx, auth_json, account_id)

        mcp = api.McpAPI(account_id, ctx.epic)
        manager = profiles.ProfileManager(mcp)

        await daily_quests_cli.main(ctx, manager)
        await llamas_cli.main(ctx, manager)
        await junk_cleaner_cli.main(ctx, manager)
        await item_shop_cli.main(ctx, manager)

    ctx.log.toggle_webhooks(False)
