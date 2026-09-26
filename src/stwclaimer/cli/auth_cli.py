import questionary
import auth
import webbrowser
import core
from cli import utils_cli


async def add_account(ctx: core.Context) -> None:
    print(ctx.ast.get_ui_str("auth_cli.add_account.info").format(auth.AUTH_CODE_LINK))
    open_in_browser = await questionary.confirm(
        ctx.ast.get_ui_str("auth_cli.add_account.askbrowser")
    ).ask_async()

    if open_in_browser:
        webbrowser.open(auth.AUTH_CODE_LINK)

    while True:
        auth_code = await questionary.password(
            ctx.ast.get_ui_str("auth_cli.add_account.pastecode")
        ).ask_async()
        if auth_code is None:
            return

        try:
            display_name = await auth.add_account(ctx.auth, auth_code)
            print(
                ctx.ast.get_ui_str("auth_cli.add_account.success").format(display_name)
            )
            break
        except ValueError as e:
            print(e)


async def list_accounts(ctx: core.Context) -> None:
    auth_json = auth.read_auth()
    print(ctx.ast.get_ui_str("auth_cli.list_accounts.title"))
    counter = 1
    for account_id in auth_json:
        print(
            auth_json[account_id]["display_name"],
            end=(
                ",\n"
                if counter % 3 == 0 and counter != len(auth_json)
                else ("" if counter == len(auth_json) else ", ")
            ),
        )
        counter += 1
    input(ctx.ast.get_ui_str("auth_cli.list_accounts.pressenter"))


async def remove_account(ctx: core.Context) -> None:
    auth_json = auth.read_auth()

    while True:
        options = []
        for account_id, data in auth_json.items():
            options.append(questionary.Choice(data["display_name"], account_id))

        choice = await utils_cli.select(
            ctx, ctx.ast.get_ui_str("auth_cli.remove_account.title"), options
        )

        if choice is False or choice is None:
            break

        confirmation = await questionary.confirm(
            ctx.ast.get_ui_str("auth_cli.remove_account.confirmation").format(
                auth_json[choice]["display_name"]
            )
        ).ask_async()

        if not confirmation:
            continue

        display_name = auth_json[choice]["display_name"]
        del auth_json[choice]
        auth.save_auth(auth_json)

        print(
            ctx.ast.get_ui_str("auth_cli.remove_account.success").format(display_name)
        )


async def menu(ctx: core.Context) -> None:
    options = {
        "auth_cli.menu.addaccount": add_account,
        "auth_cli.menu.listaccounts": list_accounts,
        "auth_cli.menu.removeaccount": remove_account,
    }

    while True:
        choice = await utils_cli.select(
            ctx,
            ctx.ast.get_ui_str("auth_cli.menu.title"),
            [questionary.Choice(ctx.ast.get_ui_str(i), i) for i in options],
        )

        if choice is False or choice is None:
            break
        print()

        await options[choice](ctx)
