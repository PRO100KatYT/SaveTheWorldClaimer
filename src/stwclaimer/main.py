import sys
import auth
import asyncio
from cli import auth_cli, menu
import core


async def main():
    menu.set_and_display_title()

    context = core.Context()

    if not auth.read_auth():
        await auth_cli.add_account(context)

    await menu.main_menu(context)

    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
