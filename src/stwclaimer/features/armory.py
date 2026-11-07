import core
import profiles
from collections import defaultdict


async def can_recycle_items(manager: profiles.ProfileManager) -> bool:
    items = await manager.search_items(
        "campaign", "homebasenode:questreward_recyclecollection"
    )

    return len(items) > 0


async def filter_resource_diff(
    manager: profiles.ProfileManager, ctx: core.Context, profile_changes: list
) -> dict:
    recycle_resources = ctx.ast.data["recycle_resources"]
    profile = await manager.get_profile("campaign")

    resource_diff = defaultdict(int)

    for entry in profile_changes:
        match entry["changeType"]:
            case "itemQuantityChanged":
                diff = entry["quantity"] - entry["oldQuantity"]
                template_id = manager.get_item_template_id(
                    profile, entry["itemId"]
                ).lower()

                if not template_id in recycle_resources:
                    continue

                resource_diff[template_id] += diff

            case "itemAdded":
                item = entry["item"]

                if not item["templateId"].lower() in recycle_resources:
                    continue

                resource_diff[item["templateId"]] += item["quantity"]

    return resource_diff
