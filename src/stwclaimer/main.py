import sys
import auth
import asyncio
from cli import auth_cli


async def main():
    if not auth.read_auth():
        await auth_cli.ask_for_login()

    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
