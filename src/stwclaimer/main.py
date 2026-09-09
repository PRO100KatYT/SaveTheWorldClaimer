import sys
import auth
import asyncio
from cli import auth_cli, menu
import api


async def main():
    menu.set_and_display_title()

    epic_api = api.EpicAPI()
    auth_api = api.AuthAPI(epic_api)

    if not auth.read_auth():
        await auth_cli.add_account(auth_api)

    await menu.main_menu(epic_api, auth_api)

    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
