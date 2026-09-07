import questionary
import auth
import webbrowser
import api


async def ask_for_login(auth_api: api.AuthAPI) -> None:
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

    print("Account added.")
