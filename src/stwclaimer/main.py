import sys
import auth
import asyncio
from cli import auth_cli
import menu


async def main():
    menu.set_and_display_title()

    if not auth.read_auth():
        await auth_cli.ask_for_login()

    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
