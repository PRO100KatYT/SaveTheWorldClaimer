import core
import profiles
from features import item_shop


async def get_free_llamas(manager: profiles.ProfileManager) -> list:
    catalog = await manager.mcp.epic.get_catalog()

    xray_storefront = {}
    for storefront in catalog["storefronts"]:
        if storefront["name"].lower() == "cardpackstorepreroll":
            xray_storefront = storefront
            break

    if not xray_storefront:
        return []

    catalog_entries = xray_storefront["catalogEntries"]
    purchases_left = await item_shop.get_purchasable_offers_counts(
        manager, catalog_entries
    )

    offers = []
    for entry in catalog_entries:
        if entry["offerId"] not in purchases_left:
            continue

        if not entry["prices"][0]["finalPrice"] == 0:
            continue

        if "always" in entry["devName"].lower():
            continue

        entry2 = entry.copy()

        entry2["num_left_to_buy"] = purchases_left[entry2["offerId"]]

        offers.append(entry2)

    return offers


async def purchase_xray_llama(manager: profiles.ProfileManager, offer: dict) -> list:
    await manager.populate_prerolled_offers("campaign")

    profile_updates = await manager.purchase_catalog_entry(
        profile_id="common_core",
        offer_id=offer["offerId"],
        purchase_quantity=1,
        currency="GameItem",
        currency_subtype="AccountResource:currency_xrayllama",
        expected_total_price=0,
    )

    notifications = profile_updates.get("common_core", {}).get("notifications", [])
    if not notifications:
        return []

    return notifications[0]["lootResult"]["items"]


def get_items_to_recycle(
    ctx: core.Context, manager: profiles.ProfileManager, items: list
) -> list:
    items_to_recycle = []

    for entry in items:
        template_id = entry["itemType"].lower()
        data = ctx.ast.get_item_data(template_id)

        rarity = data["rarity"]
        weights = ctx.ast.data["rarity_weights"]
        item_type = data["type"]

        config = ctx.cfg.get_user_config(manager.mcp.account_id)["llama_loot_recycling"]

        if item_type not in config:
            continue

        if config[item_type] == "off":
            continue

        if weights[rarity] > weights[config[item_type]]:
            continue

        items_to_recycle.append(entry)

    return items_to_recycle


async def recycle_llama_loot(
    ctx: core.Context, manager: profiles.ProfileManager, items_to_recycle: list
) -> list:
    profile_updates = await manager.recycle_item_batch(
        "campaign", [entry["itemGuid"] for entry in items_to_recycle]
    )
    profile_changes = manager.get_profile_changes(profile_updates, "campaign")

    return profile_changes
