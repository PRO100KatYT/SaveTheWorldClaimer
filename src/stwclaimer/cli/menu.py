import os
import sys
import questionary
from cli import auth_cli, utils_cli
import api


def set_and_display_title() -> None:
    if os.name == "nt":
        os.system("title Save the World Claimer")
    else:
        print("\033]0;Save the World Claimer\007", end="", flush=True)
    print("Save the World Claimer v2.0.0 by PRO100KatYT\n")


async def main_menu(epic_api: api.EpicAPI, auth_api: api.AuthAPI) -> None:
    options = {"Start this program": False, "Manage accounts": auth_cli.menu}

    while True:
        choice = await utils_cli.select("Main Menu:", options.keys(), "Exit")

        if choice is False or options[choice] is False:
            break

        await options[choice](epic_api, auth_api)
