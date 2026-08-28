import questionary
import auth
import webbrowser


async def ask_for_login():
    print(f"To add an account, log in using this link: {auth.AUTH_CODE_LINK}")
    open_in_browser = await questionary.confirm(
        "Would you like to open it in your browser?"
    ).ask_async()

    if open_in_browser:
        webbrowser.open(auth.AUTH_CODE_LINK)

    auth_code = await questionary.password(
        "Paste the authorizationCode here:"
    ).ask_async()

    await auth.add_account(auth_code)

    print("Account added.")
