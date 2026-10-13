import profiles
import utils
from collections import defaultdict
from datetime import timedelta


async def get_offers_purchases_quantities(manager: profiles.ProfileManager) -> dict:
    limits = {"daily": 1, "weekly": 7, "monthly": 30}

    count_json = defaultdict(int)

    common_core = await manager.get_profile("common_core")

    for key in common_core["items"]:
        if (
            not common_core["items"][key]["templateId"].lower()
            == "eventpurchasetracker:generic_instance"
        ):
            continue

        attributes = common_core["items"][key]["attributes"]

        if not "event_purchases" in attributes:
            continue

        for offer_id in attributes["event_purchases"]:
            count_json[offer_id] += attributes["event_purchases"][offer_id]

    common_core_attr = common_core["stats"]["attributes"]

    for limit_type in limits:
        if not f"{limit_type}_purchases" in common_core_attr:
            continue

        purchases = common_core_attr[f"{limit_type}_purchases"]

        if "lastInterval" not in purchases or "purchaseList" not in purchases:
            continue

        if utils.is_past_iso_date(
            purchases["lastInterval"], timedelta(days=limits[limit_type])
        ):
            continue

        for offer_id in purchases["purchaseList"]:
            count_json[offer_id] += purchases["purchaseList"][offer_id]

    return count_json


def get_offers_purchases_limits(catalog_entries: list) -> dict:
    count_json = defaultdict(int)
    for entry in catalog_entries:
        offer_id = entry["offerId"]

        meta_info = entry.get("metaInfo", [])
        for info in meta_info:
            if info["key"].lower() == "eventlimit":
                count_json[offer_id] += int(info["value"])

        for limit_type in ["dailyLimit", "weeklyLimit", "monthlyLimit"]:
            if not limit_type in entry:
                continue
            if entry[limit_type] <= 0:
                continue

            count_json[offer_id] += entry[limit_type]

    return count_json


async def get_purchasable_offers_counts(
    manager: profiles.ProfileManager, catalog_entries: list
) -> dict:
    purchases_quantities = await get_offers_purchases_quantities(manager)
    purchases_limits = get_offers_purchases_limits(catalog_entries)

    count_json = defaultdict(int)

    for entry in catalog_entries:
        offer_id = entry["offerId"]

        left_to_purchase = purchases_limits[offer_id] - purchases_quantities[offer_id]
        if left_to_purchase > 0:
            count_json[offer_id] = left_to_purchase

    return count_json
