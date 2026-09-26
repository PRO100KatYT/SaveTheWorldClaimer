import os
from cli import auth_cli, utils_cli
from features import claimer
import core
import questionary


def set_and_display_title(version: str) -> None:
    if os.name == "nt":
        os.system("title Save the World Claimer")
    else:
        print("\033]0;Save the World Claimer\007", end="", flush=True)
    print(f"Save the World Claimer v{version} by PRO100KatYT\n")


async def main_menu(ctx: core.Context) -> None:

    options = {
        "menu.main_menu.start": claimer.loop,
        "menu.main_menu.manageaccounts": auth_cli.menu,
    }

    while True:
        choice = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("menu.main_menu.title"),
            [questionary.Choice(ctx.ast.get_ui_str(i), i) for i in options],
            ctx.ast.get_ui_str("menu.main_menu.exit"),
        )

        if choice is False or options[choice] is False:
            break

        await options[choice](ctx)
