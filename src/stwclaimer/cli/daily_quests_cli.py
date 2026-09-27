import core
import profiles
from features import daily_quests
from cli import utils_cli
import auth


def display_quests(ctx: core.Context, quests: dict, receive_mtx: bool) -> None:
    counter = 0

    if not quests:
        print(ctx.ast.get_ui_str("daily_quests_cli.noquests"))

    for quest_id in quests["daily_quest_items"]:
        counter += 1
        name, objectives, rewards = daily_quests.get_quest_parts(
            ctx, quests["daily_quest_items"][quest_id], receive_mtx
        )

        if quest_id in quests["new_quest_ids"]:
            quest_string = ctx.ast.get_ui_str("daily_quests_cli.displaynew")
        else:
            quest_string = ctx.ast.get_ui_str("daily_quests_cli.display")

        print(quest_string.format(counter, name, objectives, rewards))

    print()


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    print(ctx.ast.get_ui_str("daily_quests_cli.fetching"))

    await manager.query_profile("campaign")
    profile_updates = await manager.client_quest_login("campaign")
    profile_changes = manager.get_profile_changes(profile_updates, "campaign")

    quests = daily_quests.get_daily_quests(manager, profile_changes)

    receive_mtx = await daily_quests.can_receive_mtx(manager)
    display_quests(ctx, quests, receive_mtx)


async def menu(ctx: core.Context) -> None:
    auth_json = auth.read_auth()

    while True:
        choice = await utils_cli.select_account(
            ctx, auth_json, ctx.ast.get_ui_str("daily_quests_cli.select_account.title")
        )

        if choice is False or choice is None:
            break

        await utils_cli.login_with_printing(ctx, auth_json, choice)
