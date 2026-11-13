import profiles
import utils
import config
from collections import defaultdict
from datetime import timedelta


async def get_offers_purchases_quantities(manager: profiles.ProfileManager) -> dict:
    limits = {"daily": 1, "weekly": 7, "monthly": 30}

    count_json = defaultdict(int)

    purchase_trackers = await manager.search_items(
        "common_core", "eventpurchasetracker:generic_instance", {"event_purchases": any}
    )

    common_core = await manager.get_profile("common_core")

    for key in purchase_trackers:
        attributes = common_core["items"][key]["attributes"]

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


def get_eligible_items_criteria(user_config: dict) -> list:
    def crawl(data_part: dict, user_config: dict, criteria: list) -> None:
        for key in data_part:
            if "eligible_shop_items" in data_part[key]:
                if not user_config[key]:
                    continue
                criteria.append(data_part[key]["eligible_shop_items"])
            else:
                if "content" in data_part[key]:
                    crawl(data_part[key]["content"], user_config[key], criteria)

    criteria = []
    crawl(
        config.USER_CONFIG_DATA["item_shop_purchaser"]["content"], user_config, criteria
    )

    return criteria


def is_entry_eligible(criteria: list, catalog_entry: dict) -> bool:
    for criteria_set in criteria:
        for item in catalog_entry["itemGrants"]:
            criteria_met = 0
            template_id = item["templateId"].lower()

            for criterion in criteria_set:
                match criterion:
                    case "template_ids":
                        if template_id in criteria_set["template_ids"]:
                            criteria_met += 1
                    case "starts_with":
                        if any(
                            template_id.startswith(entry)
                            for entry in criteria_set["starts_with"]
                        ):
                            criteria_met += 1
                    case "contains":
                        if any(
                            entry.lower() in template_id
                            for entry in criteria_set["contains"]
                        ):
                            criteria_met += 1

                if criteria_met == len(criteria_set):
                    return True

    return False


async def deny_on_ownership_num_left(
    manager: profiles.ProfileManager, catalog_entry: dict
) -> int | None:
    if not catalog_entry.get("requirements", []):
        return
    requirement = catalog_entry["requirements"][0]

    if requirement["requirementType"].lower() != "denyonitemownership":
        return

    quantity = requirement["minQuantity"]
    template_id = requirement["requiredId"].lower()

    profile = await manager.get_profile("campaign")
    guids = await manager.search_items("campaign", template_id)

    for guid in guids:
        quantity -= profile["items"][guid]["quantity"]

    if quantity < 0:
        quantity = 0

    return quantity


async def get_catalog_offers_to_purchase(
    manager: profiles.ProfileManager, user_config: dict
) -> list:
    catalog = await manager.mcp.epic.get_catalog()
    criteria = get_eligible_items_criteria(user_config)
    offers = []

    for storefront in catalog["storefronts"]:
        if storefront["name"].lower() not in [
            "stwrotationaleventstorefront",
            "stwspecialeventstorefront",
        ]:
            continue

        catalog_entries = storefront["catalogEntries"]
        purchases_left = await get_purchasable_offers_counts(manager, catalog_entries)

        for entry in catalog_entries:
            if entry["offerId"] not in purchases_left:
                continue

            if (
                not entry["prices"][0]["currencySubType"].lower()
                == "accountresource:eventcurrency_scaling"
            ):
                continue

            if not is_entry_eligible(criteria, entry):
                continue

            num_left_to_buy = purchases_left[entry["offerId"]]
            ownership_left = await deny_on_ownership_num_left(manager, entry)

            if ownership_left is not None:
                num_left_to_buy = min(num_left_to_buy, ownership_left)

            if num_left_to_buy <= 0:
                continue

            entry2 = entry.copy()

            entry2["num_left_to_buy"] = num_left_to_buy

            offers.append(entry2)

    return offers


async def get_gold_quantity(manager: profiles.ProfileManager) -> int:
    guids = await manager.search_items(
        "campaign", "accountresource:eventcurrency_scaling"
    )
    if not guids:
        return 0

    profile = await manager.get_profile("campaign")

    return profile["items"][guids[0]].get("quantity", 0)


async def get_affordable_purchase_quantity(
    manager: profiles.ProfileManager, offer: dict, user_config: dict
) -> int:
    min_gold_threshold = user_config["gold"]["dont_spend_below"]
    owned_gold = await get_gold_quantity(manager)
    left_to_buy = offer["num_left_to_buy"]
    unit_price = offer["prices"][0]["finalPrice"]

    return min(
        left_to_buy, max(owned_gold - min_gold_threshold, 0) // max(unit_price, 1)
    )


async def purchase_catalog_offer(
    manager: profiles.ProfileManager, offer: dict, purchase_quantity: int
) -> dict:
    profile_updates = await manager.purchase_catalog_entry(
        profile_id="common_core",
        offer_id=offer["offerId"],
        purchase_quantity=purchase_quantity,
        currency=offer["prices"][0]["currencyType"],
        currency_subtype=offer["prices"][0]["currencySubType"],
        expected_total_price=offer["prices"][0]["finalPrice"] * purchase_quantity,
    )

    return profile_updates
