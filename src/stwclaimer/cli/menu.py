import os
from cli import auth_cli, utils_cli
from features import claimer
import core


def set_and_display_title() -> None:
    if os.name == "nt":
        os.system("title Save the World Claimer")
    else:
        print("\033]0;Save the World Claimer\007", end="", flush=True)
    print("Save the World Claimer v2.0.0 by PRO100KatYT\n")


async def main_menu(context: core.Context) -> None:
    options = {"Start this program": claimer.loop, "Manage accounts": auth_cli.menu}

    while True:
        choice = await utils_cli.select("Main Menu:", options.keys(), "Exit")

        if choice is False or options[choice] is False:
            break

        await options[choice](context)
