import profiles


def is_active_daily_quest(item: dict) -> bool:
    return (
        item["templateId"].lower().startswith("quest:daily_")
        and item["attributes"]["quest_state"].lower() == "active"
    )


def get_daily_quests(manager: profiles.ProfileManager, profile_changes: list) -> dict:
    output = {"new_quests": {}, "quests": {}}

    for change in profile_changes:
        if not change["changeType"] == "itemAdded":
            continue
        if not is_active_daily_quest(change["item"]):
            continue
        output["new_quests"][change["itemId"]] = change["item"]

    for guid, item in manager.cache["campaign"]["items"].items():
        if not is_active_daily_quest(item):
            continue
        if guid in output["new_quests"]:
            continue

        output["quests"][guid] = item

    return output


async def main(manager: profiles.ProfileManager) -> None:
    await manager.query_profile("campaign")
    profile_updates = await manager.client_quest_login("campaign")
    profile_changes = manager.get_profile_changes(profile_updates, "campaign")

    daily_quests = get_daily_quests(manager, profile_changes)

    print(daily_quests)
