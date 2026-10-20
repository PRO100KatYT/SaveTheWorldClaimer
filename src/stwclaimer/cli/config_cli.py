import core
from cli import utils_cli
import questionary
import config
import auth
import config


async def ask_for_new_value(ctx: core.Context, option_data: dict, current_value):
    if option_data["valid_values"]:
        new_value = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("config_cli.ask_for_value.select").format(
                ctx.ast.get_ui_str(option_data["description"])
            ),
            [
                questionary.Choice(
                    str(i),
                    i,
                )
                for i in option_data["valid_values"]
            ],
            start=current_value,
            add_back=False,
        )
    else:
        new_value = await questionary.text(
            ctx.ast.get_ui_str("config_cli.ask_for_value.input").format(
                ctx.ast.get_ui_str(option_data["description"])
            ),
            option_data["default"],
            validate=lambda text: utils_cli.validate_type(text, option_data["type"]),
        ).ask_async()

    return new_value


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
                    "config_cli.ask_for_value.entry_disabled"
                ).format(display_name)
            else:
                options[option] = ctx.ast.get_ui_str(
                    "config_cli.ask_for_value.entry_value"
                ).format(display_name, value)

        choice = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("config_cli.ask_for_value.title"),
            [questionary.Choice(options[i], i) for i in options],
            start=last_selected_option,
        )

        if choice is False or choice is None:
            break

        last_selected_option = choice
        new_value = await ask_for_new_value(
            ctx,
            config.GLOBAL_CONFIG_DATA[choice],
            ctx.cfg.global_config[choice],
        )
        ctx.cfg.set_global_value(choice, new_value)


async def account_menu(ctx: core.Context) -> None:
    auth_json = auth.read_auth()
    last_selected_option = None

    while True:
        choice = await utils_cli.select_account(
            ctx, auth_json, ctx.ast.get_ui_str("config_cli.account_menu.title")
        )

        if choice is False or choice is None:
            break

        user_config = ctx.cfg.get_user_config(choice)

        current_config_path = []

        while True:
            data_part = config.USER_CONFIG_DATA
            config_part = user_config
            for entry in current_config_path:
                data_part = data_part[entry]["content"]
                config_part = config_part[entry]

            options = {}
            for key in data_part:
                display_name = ctx.ast.get_ui_str(data_part[key]["display_name"])

                if "type" in data_part[key]:
                    value = config_part[key]
                    if value == "":
                        options[key] = ctx.ast.get_ui_str(
                            "config_cli.ask_for_value.entry_disabled"
                        ).format(display_name)
                    else:
                        options[key] = ctx.ast.get_ui_str(
                            "config_cli.ask_for_value.entry_value"
                        ).format(display_name, value)
                else:
                    options[key] = display_name

            choice2 = await utils_cli.select(
                ctx,
                ctx.ast.get_ui_str("config_cli.account_menu.settings").format(
                    auth_json[choice]["display_name"]
                ),
                [questionary.Choice(options[i], i) for i in options],
                start=last_selected_option,
            )

            if choice2 is False or choice2 is None:
                if not current_config_path:
                    break
                else:
                    current_config_path.pop()
                    last_selected_option = None
                    continue

            current_config_path.append(choice2)
            last_selected_option = choice2

            if "type" in data_part[choice2]:
                new_value = await ask_for_new_value(
                    ctx,
                    data_part[choice2],
                    config_part[choice2],
                )
                ctx.cfg.set_user_value(choice, current_config_path, new_value)

                current_config_path.pop()
            else:
                last_selected_option = None


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
