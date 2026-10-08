import questionary
import core
import auth


async def login_with_printing(
    ctx: core.Context, auth_json: dict, account_id: str
) -> None:
    display_name = auth_json[account_id]["display_name"]
    ctx.log.message(
        ctx.ast.get_ui_str("utils_cli.login.loggingin").format(display_name), end=" "
    )

    await auth.login(ctx.auth, account_id, auth_json)

    ctx.log.message(ctx.ast.get_ui_str("utils_cli.login.success"), hide_date_time=True)


async def select(
    ctx: core.Context, title: str, options: list, back_str: str | None = None
) -> str:
    options = list(options)
    options.append(
        questionary.Choice(
            ctx.ast.get_ui_str("select.back") if back_str is None else back_str,
            False,
            shortcut_key="0",
        )
    )

    return await questionary.select(
        title,
        options,
        qmark="",
        pointer=">",
        use_shortcuts=True,
        instruction=" ",
    ).ask_async()


async def select_account(ctx: core.Context, auth_json: dict, title: str) -> str:
    options = []
    for account_id, data in auth_json.items():
        options.append(questionary.Choice(data["display_name"], account_id))

    choice = await select(ctx, title, options)

    return choice
