import profiles
import core


def is_active_daily_quest(item: dict) -> bool:
    return (
        item["templateId"].lower().startswith("quest:daily_")
        and item["attributes"]["quest_state"].lower() == "active"
    )


def get_daily_quests(manager: profiles.ProfileManager, profile_changes: list) -> dict:
    output = {"new_quest_ids": [], "daily_quest_items": {}}

    for change in profile_changes:
        if not change["changeType"] == "itemAdded":
            continue
        if not is_active_daily_quest(change["item"]):
            continue
        output["new_quest_ids"].append(change["itemId"])

    for guid, item in manager.cache["campaign"]["items"].items():
        if not is_active_daily_quest(item):
            continue

        output["daily_quest_items"][guid] = item

    return output


def get_quest_parts(ctx: core.Context, item: dict) -> str:
    name = ctx.ast.get_item_str(item["templateId"].lower())
    quest_data = ctx.ast.data["items"][item["templateId"].lower()]

    objectives = []
    for objective in quest_data["objectives"]:
        user_completion = item["attributes"].get(f"completion_{objective}", 0)
        max_completion = quest_data["objectives"][objective]["count"]
        objective_name = ctx.ast.get_objective_str(objective)

        objectives.append(f"{user_completion}/{max_completion} {objective_name}")
    objectives = ", ".join(objectives)

    rewards = []
    for template_id in quest_data["rewards"]:
        template_id = template_id.lower()

        if template_id.startswith("conditionalresource:"):
            reward_names = [
                ctx.ast.get_item_str(template_id)["PassedConditionItem"],
                ctx.ast.get_item_str(template_id)["FailedConditionItem"],
            ]
        else:
            reward_names = [ctx.ast.get_item_str(template_id)]

        for reward_name in reward_names:
            rewards.append(f"{quest_data['rewards'][template_id]}x {reward_name}")
    rewards = ", ".join(rewards)

    return (name, objectives, rewards)


def display_quests(ctx: core.Context, daily_quests: dict) -> None:
    counter = 0

    if not daily_quests:
        print(ctx.ast.get_ui_str("daily_quests.noquests"))

    for quest_id in daily_quests["daily_quest_items"]:
        counter += 1
        name, objectives, rewards = get_quest_parts(
            ctx, daily_quests["daily_quest_items"][quest_id]
        )

        if quest_id in daily_quests["new_quest_ids"]:
            quest_string = ctx.ast.get_ui_str("daily_quests.displaynew")
        else:
            quest_string = ctx.ast.get_ui_str("daily_quests.display")

        print(quest_string.format(counter, name, objectives, rewards))

    print()


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    await manager.query_profile("campaign")
    profile_updates = await manager.client_quest_login("campaign")
    profile_changes = manager.get_profile_changes(profile_updates, "campaign")

    print(ctx.ast.get_ui_str("daily_quests.fetching"))
    daily_quests = get_daily_quests(manager, profile_changes)

    display_quests(ctx, daily_quests)
