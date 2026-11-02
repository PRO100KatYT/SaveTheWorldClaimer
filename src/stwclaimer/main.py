import sys
import auth
import asyncio
from cli import auth_cli, menu
import core

VERSION = "2.0.0"


async def main():
    menu.set_and_display_title(VERSION)

    ctx = core.Context()
    asyncio.create_task(ctx.log.webhook_loop())

    if not auth.read_auth():
        await auth_cli.add_account(ctx)

    await menu.main_menu(ctx)

    await ctx.epic.session.aclose()
    await ctx.log.webhook_session.aclose()

    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
