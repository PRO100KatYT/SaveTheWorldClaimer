import questionary
import auth
import webbrowser
import api


async def add_account(auth_api: api.AuthAPI) -> None:
    print(f"To add an account, log in using this link: {auth.AUTH_CODE_LINK}")
    open_in_browser = await questionary.confirm(
        "Would you like to open it in your browser?"
    ).ask_async()

    if open_in_browser:
        webbrowser.open(auth.AUTH_CODE_LINK)

    while True:
        auth_code = await questionary.password(
            "Paste the authorizationCode here:"
        ).ask_async()
        if auth_code is None:
            return

        try:
            await auth.add_account(auth_api, auth_code)
            break
        except ValueError as e:
            print(e)

    print("\nAccount added.\n")


async def list_accounts(*args) -> None:
    auth_json = auth.read_auth()
    print("Added accounts:")
    counter = 1
    for account in auth_json:
        print(
            account["display_name"],
            end=(
                ",\n"
                if counter % 3 == 0 and counter != len(auth_json)
                else ("" if counter == len(auth_json) else ", ")
            ),
        )
        counter += 1
    input("\n\nPress ENTER to continue.\n")


async def menu(epic_api: api.EpicAPI, auth_api: api.AuthAPI) -> None:
    options = {
        "Add an account": add_account,
        "List accounts": list_accounts,
        "Remove an account": None,
        "Back": None,
    }

    while True:
        choice = await questionary.select(
            "Account Management:",
            options.keys(),
            qmark="",
            pointer=">",
            use_shortcuts=True,
            instruction=" ",
        ).ask_async()

        if choice is None or options[choice] is None:
            break
        print()

        await options[choice](auth_api)
