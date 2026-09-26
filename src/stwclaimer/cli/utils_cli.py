import questionary
import core


async def select(
    ctx: core.Context, title: str, options: list, back_str: str = None
) -> str:
    options = list(options)
    options.append(
        questionary.Choice(
            ctx.ast.get_ui_str("select.back") if back_str is None else back_str, False, shortcut_key="0"
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
