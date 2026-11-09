import core
import profiles

TIERS = {
    1: [],
    2: ["t01"],
    3: ["t01", "t02"],
    4: ["t01", "t02", "t03"],
    5: ["t01", "t02", "t03", "t04"],
}


async def save_backpack_snapshot(
    ctx: core.Context, manager: profiles.ProfileManager
) -> None:
    theater0 = await manager.get_profile("theater0")
    snapshot = []

    for guid in theater0["items"]:
        template_id = manager.get_item_template_id(theater0, guid).lower()
        item_type = manager.get_type_from_template_id(template_id)

        if item_type in ["weapon", "trap"]:
            snapshot.append(guid)

    # Saving this as a string prevents it from taking a huge part of the file's vertical space
    snapshot_str = ",".join(snapshot)

    ctx.cfg.set_user_value(
        manager.mcp.account_id,
        ["inventory_junk_cleaner", "backpack_snapshot"],
        snapshot_str,
    )


async def search_for_items(
    ctx: core.Context, manager: profiles.ProfileManager, user_config: dict
) -> tuple:
    guids_to_recycle = []
    guids_to_destroy = []

    snapshot_str = user_config["backpack_snapshot"]
    snapshot = snapshot_str.split(",") if snapshot_str else []

    tier_config, power_level_config = user_config["tier"], user_config["power_level"]

    profile = await manager.get_profile("theater0")

    for key in profile["items"]:
        template_id, attributes, quantity = [
            profile["items"][key].get("templateId", "").lower(),
            profile["items"][key].get("attributes", {}),
            profile["items"][key].get("quantity", 0),
        ]
        item_type = manager.get_type_from_template_id(template_id)

        if item_type == "ingredient":
            item_tier = ctx.ast.data["items"].get(template_id, {}).get("tier", "")
            if item_tier in TIERS[tier_config]:
                guids_to_destroy.append(key)
        elif (
            item_type in ["weapon", "trap"]
            and key not in snapshot
            and (not template_id.startswith("weapon:buildingitemdata"))
        ):
            power_level = ctx.ast.get_item_power_level(
                template_id, attributes.get("level", 50)
            )
            if power_level < power_level_config:
                guids_to_recycle.append({"itemId": key, "quantity": quantity})

    return (guids_to_recycle, guids_to_destroy)
