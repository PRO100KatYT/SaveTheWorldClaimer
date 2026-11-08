import os
from cli import auth_cli, utils_cli, daily_quests_cli, config_cli
from cli import claimer
import core
import questionary
from datetime import datetime


def get_seasonal_greeting(ctx: core.Context) -> str:
    now = datetime.now()
    day, month, year = now.day, now.month, now.year

    if month == 11 and day == 8:
        age = year - 2021
        suffix = utils_cli.get_ordinal_suffix(age, ctx.cfg.global_config["ui_language"])
        return ctx.ast.get_ui_str("menu.greeting.claimer_birthday").format(age, suffix)

    if month == 12 and day in (24, 25, 26):
        return ctx.ast.get_ui_str("menu.greeting.merry_christmas")

    if (month == 12 and day == 31) or (month == 1 and day == 1):
        return ctx.ast.get_ui_str("menu.greeting.happy_new_year")

    return ""


def set_and_display_title(version: str) -> None:
    if os.name == "nt":
        os.system("title Save the World Claimer")
    else:
        print("\033]0;Save the World Claimer\007", end="", flush=True)
    print(f"Save the World Claimer v{version} by PRO100KatYT\n")


async def main_menu(ctx: core.Context) -> None:
    options = {
        "menu.main_menu.start": claimer.loop,
        "menu.main_menu.dailyquests": daily_quests_cli.menu,
        "menu.main_menu.manageaccounts": auth_cli.menu,
        "menu.main_menu.settings": config_cli.menu,
    }

    greeting = get_seasonal_greeting(ctx)
    if greeting:
        ctx.log.message(greeting, hide_date_time=True)

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
