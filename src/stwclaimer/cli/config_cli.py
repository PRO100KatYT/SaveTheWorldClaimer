import core
from cli import utils_cli
import questionary
import config


async def change_setting(ctx: core.Context, option: str) -> None:
    option_data = config.GLOBAL_CONFIG_DATA[option]
    if option_data["valid_values"]:
        new_value = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("config_cli.general_menu.select").format(
                ctx.ast.get_ui_str(option_data["description"])
            ),
            [
                questionary.Choice(
                    str(i),
                    i,
                )
                for i in option_data["valid_values"]
            ],
            start=ctx.cfg.global_config[option],
            add_back=False,
        )
    else:
        new_value = await questionary.text(
            ctx.ast.get_ui_str("config_cli.general_menu.input").format(
                ctx.ast.get_ui_str(option_data["description"])
            ),
            option_data["default"],
            validate=lambda text: utils_cli.validate_type(text, option_data["type"]),
        ).ask_async()

    ctx.cfg.set_global_value(option, new_value)


async def general_menu(ctx: core.Context) -> None:
    last_selected_option = None

    while True:
        options = {}
        for option in config.GLOBAL_CONFIG_DATA:
            display_name = ctx.ast.get_ui_str(
                config.GLOBAL_CONFIG_DATA[option]["display_name"]
            )
            value = ctx.cfg.global_config[option]

            if value == "":
                options[option] = ctx.ast.get_ui_str(
                    "config_cli.general_menu.entry_disabled"
                ).format(display_name)
            else:
                options[option] = ctx.ast.get_ui_str(
                    "config_cli.general_menu.entry_value"
                ).format(display_name, value)

        choice = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("config_cli.general_menu.title"),
            [questionary.Choice(options[i], i) for i in options],
            start=last_selected_option,
        )

        if choice is False or choice is None:
            break

        last_selected_option = choice
        await change_setting(ctx, choice)


async def account_menu(ctx: core.Context) -> None:
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

        await options[choice](ctx)
