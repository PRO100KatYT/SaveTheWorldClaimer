import questionary
import auth
import webbrowser
import api
from cli import utils_cli


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
            display_name = await auth.add_account(auth_api, auth_code)
            print(f"\n{display_name} has been added to the program.\n")
            break
        except ValueError as e:
            print(e)


async def list_accounts(*args) -> None:
    auth_json = auth.read_auth()
    print("Added accounts:")
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
    input("\n\nPress ENTER to continue.\n")


async def remove_account(*args) -> None:
    auth_json = auth.read_auth()

    while True:
        options = []
        for account_id, data in auth_json.items():
            options.append(questionary.Choice(data["display_name"], account_id))

        choice = await utils_cli.select("Select an account to remove:", options)

        if choice is False or choice is None:
            break

        confirmation = await questionary.confirm(
            f"Are you sure you want to remove {auth_json[choice]["display_name"]} from the program?"
        ).ask_async()

        if not confirmation:
            continue

        display_name = auth_json[choice]["display_name"]
        del auth_json[choice]
        auth.save_auth(auth_json)

        print(f"\nSuccessfully removed {display_name} from the program.\n")


async def menu(epic_api: api.EpicAPI, auth_api: api.AuthAPI) -> None:
    options = {
        "Add an account": add_account,
        "List accounts": list_accounts,
        "Remove an account": remove_account,
    }

    while True:
        choice = await utils_cli.select("Account Management:", options)

        if choice is False or choice is None:
            break
        print()

        await options[choice](auth_api)
