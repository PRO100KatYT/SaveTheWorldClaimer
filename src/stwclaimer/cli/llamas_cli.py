from features import llamas
import core
import profiles
from features import inventory


def sort_loot_by_rarity(ctx: core.Context, loot_result: list) -> list:
    weights = ctx.ast.data["rarity_weights"]
    return sorted(
        loot_result,
        key=lambda item: weights.get(
            ctx.ast.data.get("items", {})
            .get(item["itemType"].lower(), {})
            .get("rarity", "common"),
            0,
        ),
    )


def format_and_print_loot(ctx: core.Context, loot_result: list) -> None:
    loot_result = sort_loot_by_rarity(ctx, loot_result)

    counter = 0
    for entry in loot_result:
        counter += 1
        template_id = entry["itemType"].lower()
        item_data = ctx.ast.get_item_data(template_id)

        rarity = ctx.ast.get_rarity_str(item_data["rarity"])
        color = ctx.ast.get_rarity_color(item_data["rarity"])

        item_type = ctx.ast.get_type_str(item_data["type"])
        item_name = ctx.ast.get_item_str(template_id)

        ctx.log.message(
            f"{counter}: [{color}]{rarity} | {item_type}: {entry['quantity']}x {item_name}[/]"
        )


async def open_llama(
    ctx: core.Context, manager: profiles.ProfileManager, offer: dict, llama_loot: list
) -> None:
    template_id = offer["itemGrants"][0]["templateId"].lower()
    llama_name = ctx.ast.get_item_str(template_id)

    ctx.log.message(
        ctx.ast.get_ui_str("llamas_cli.main.opening").format(llama_name), end=" "
    )

    loot_items = await llamas.purchase_xray_llama(manager, offer)
    llama_loot.extend(loot_items)

    ctx.log.message(ctx.ast.get_ui_str("llamas_cli.main.success"), hide_date_time=True)

    format_and_print_loot(ctx, loot_items)


def format_resource_diff(resource_diff: dict) -> list:
    result = []

    for template_id in resource_diff:
        result.append({"itemType": template_id, "quantity": resource_diff[template_id]})

    return result


async def recycle_loot(
    ctx: core.Context, manager: profiles.ProfileManager, llama_loot: list
) -> None:
    can_recycle_items = await inventory.can_recycle_items(manager)
    if not can_recycle_items:
        ctx.log.message(ctx.ast.get_ui_str("llamas_cli.recycling.unavailable"))
        return

    items_to_recycle = llamas.get_items_to_recycle(ctx, manager, llama_loot)

    if not items_to_recycle:
        return

    ctx.log.message("Recycling the following items:")
    format_and_print_loot(ctx, items_to_recycle)
    ctx.log.message()

    profile_changes = await llamas.recycle_llama_loot(ctx, manager, items_to_recycle)

    resource_diff = await inventory.filter_resource_diff(manager, ctx, profile_changes)
    diff_formatted = format_resource_diff(resource_diff)

    ctx.log.message("Resources gained:")
    format_and_print_loot(ctx, diff_formatted)
    ctx.log.message()


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    if not ctx.cfg.global_config["open_free_llamas"]:
        return

    await manager.get_profile("campaign")

    free_llama_offers = await llamas.get_free_llamas(manager)

    if not free_llama_offers:
        return

    total_count = sum(offer["num_left_to_buy"] for offer in free_llama_offers)

    ctx.log.message(
        ctx.ast.get_ui_str("llamas_cli.main.available").format(
            ctx.ast.get_plural_word("thereAre", total_count),
            total_count,
            ctx.ast.get_plural_word("freeLlamas", total_count),
            ctx.ast.get_plural_word("available", total_count),
        )
    )

    llama_loot = []
    for offer in free_llama_offers:
        for _ in range(offer["num_left_to_buy"]):
            await open_llama(ctx, manager, offer, llama_loot)

    await recycle_loot(ctx, manager, llama_loot)
