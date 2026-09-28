import profiles
import core


async def can_receive_mtx(manager: profiles.ProfileManager) -> bool:
    profile = await manager.get_profile("common_core")
    for item_id in profile["items"]:
        if (
            profile["items"][item_id]["templateId"].lower()
            == "token:receivemtxcurrency"
        ):
            return True
    return False


async def get_quest_rerolls(manager: profiles.ProfileManager) -> int:
    profile = await manager.get_profile("campaign")
    attributes = profile["stats"]["attributes"]

    return attributes.get("quest_manager", {}).get("dailyQuestRerolls", 0)


def is_active_daily_quest(item: dict) -> bool:
    return (
        item["templateId"].lower().startswith("quest:daily_")
        and item["attributes"]["quest_state"].lower() == "active"
    )


async def get_daily_quests(
    manager: profiles.ProfileManager, profile_changes: list = []
) -> dict:
    output = {"new_quest_ids": [], "daily_quest_items": {}}

    for change in profile_changes:
        if not change["changeType"] == "itemAdded":
            continue
        if not is_active_daily_quest(change["item"]):
            continue
        output["new_quest_ids"].append(change["itemId"])

    profile = await manager.get_profile("campaign")

    for guid in profile["items"]:
        if not is_active_daily_quest(profile["items"][guid]):
            continue

        output["daily_quest_items"][guid] = profile["items"][guid]

    return output


def get_quest_parts(ctx: core.Context, item: dict, receive_mtx: bool) -> str:
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
            reward_names = [ctx.ast.get_item_str(template_id)["FailedConditionItem"]]

            if receive_mtx:
                reward_names.insert(
                    0, ctx.ast.get_item_str(template_id)["PassedConditionItem"]
                )
        else:
            reward_names = [ctx.ast.get_item_str(template_id)]

        for reward_name in reward_names:
            rewards.append(f"{quest_data['rewards'][template_id]}x {reward_name}")
    rewards = ", ".join(rewards)

    return (name, objectives, rewards)
