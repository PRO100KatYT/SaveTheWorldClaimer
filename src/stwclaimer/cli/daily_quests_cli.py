import core
import profiles
from features import daily_quests
from cli import utils_cli
import auth
import api
import questionary


def display_quests(ctx: core.Context, quests: dict, receive_mtx: bool) -> None:
    counter = 0

    if not quests["daily_quest_items"]:
        ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.noquests"))

    for quest_id in quests["daily_quest_items"]:
        counter += 1
        name, objectives, rewards = daily_quests.get_quest_parts(
            ctx, quests["daily_quest_items"][quest_id], receive_mtx
        )

        if quest_id in quests["new_quest_ids"]:
            quest_string = ctx.ast.get_ui_str("daily_quests_cli.displaynew")
        else:
            quest_string = ctx.ast.get_ui_str("daily_quests_cli.display")

        ctx.log.message(quest_string.format(counter, name, objectives, rewards))

    ctx.log.message()


async def select_daily_quest(
    ctx: core.Context, quests: dict, receive_mtx: bool
) -> None:
    if not quests:
        ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.noquests"))

    options = []

    for quest_id in quests["daily_quest_items"]:
        name, objectives, rewards = daily_quests.get_quest_parts(
            ctx, quests["daily_quest_items"][quest_id], receive_mtx
        )

        if quest_id in quests["new_quest_ids"]:
            quest_string = ctx.ast.get_ui_str(
                "daily_quests_cli.select_daily_quest.displaynew"
            )
        else:
            quest_string = ctx.ast.get_ui_str(
                "daily_quests_cli.select_daily_quest.display"
            )

        options.append(
            questionary.Choice(quest_string.format(name, objectives, rewards), quest_id)
        )

    choice = await utils_cli.select(
        ctx, ctx.ast.get_ui_str("daily_quests_cli.select_daily_quest.title"), options
    )

    return choice


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.fetching"))

    daily_quests_unlocked = await daily_quests.can_get_daily_quests(manager)
    if not daily_quests_unlocked:
        ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.unavailable"))
        return

    profile_updates = await manager.client_quest_login("campaign")
    profile_changes = manager.get_profile_changes(profile_updates, "campaign")

    quests = await daily_quests.get_daily_quests(manager, profile_changes)

    receive_mtx = await daily_quests.can_receive_mtx(manager)
    display_quests(ctx, quests, receive_mtx)


async def select_and_replace(
    ctx: core.Context, manager: profiles.ProfileManager, profile_changes: dict
) -> None:
    while True:
        quests = await daily_quests.get_daily_quests(manager, profile_changes)
        receive_mtx = await daily_quests.can_receive_mtx(manager)
        rerolls = await daily_quests.get_quest_rerolls(manager)

        ctx.log.message()

        if rerolls == 0:
            display_quests(ctx, quests, receive_mtx)
            ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.replace.norerolls"))
            input()
        else:
            quest_id = await select_daily_quest(ctx, quests, receive_mtx)
            if quest_id is False or quest_id is None:
                break

            confirmation = await questionary.confirm(
                ctx.ast.get_ui_str("daily_quests_cli.replace.confirmation")
            ).ask_async()

            if not confirmation:
                continue

            ctx.log.message(
                ctx.ast.get_ui_str("daily_quests_cli.replace.progress"), end=" "
            )

            profile_updates = await manager.fort_reroll_daily_quest(
                "campaign", quest_id
            )
            profile_changes = manager.get_profile_changes(profile_updates, "campaign")

            ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.replace.success"))

            continue

        break


async def menu(ctx: core.Context) -> None:
    auth_json = auth.read_auth()

    while True:
        choice = await utils_cli.select_account(
            ctx, auth_json, ctx.ast.get_ui_str("daily_quests_cli.select_account.title")
        )

        if choice is False or choice is None:
            break

        await utils_cli.login_with_printing(ctx, auth_json, choice)

        mcp = api.McpAPI(choice, ctx.epic)
        manager = profiles.ProfileManager(mcp)

        daily_quests_unlocked = await daily_quests.can_get_daily_quests(manager)
        if not daily_quests_unlocked:
            ctx.log.message(ctx.ast.get_ui_str("daily_quests_cli.unavailable"))
            input(ctx.ast.get_ui_str("daily_quests_cli.pressenter"))
            continue

        profile_updates = await manager.client_quest_login("campaign")
        profile_changes = manager.get_profile_changes(profile_updates, "campaign")

        await select_and_replace(ctx, manager, profile_changes)
