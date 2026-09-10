import questionary


async def select(title: str, options: list, back_str: str = None) -> str:
    options = list(options)
    options.append(
        questionary.Choice(
            "Back" if back_str is None else back_str, False, shortcut_key="0"
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
