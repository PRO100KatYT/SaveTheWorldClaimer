import core
from cli import utils_cli
import questionary


async def general_menu(ctx: core.Context):
    return


async def account_menu(ctx: core.Context):
    return


async def menu(ctx: core.Context) -> None:
    options = {
        "config_cli.menu.general": general_menu,
        "config_cli.menu.account": account_menu,
    }

    while True:
        choice = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("config_cli.menu.title"),
            [questionary.Choice(ctx.ast.get_ui_str(i), i) for i in options],
        )

        if choice is False or choice is None:
            break
        ctx.log.message()

        await options[choice](ctx)
