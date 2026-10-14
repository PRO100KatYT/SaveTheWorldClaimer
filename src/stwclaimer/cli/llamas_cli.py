from features import llamas
import core
import profiles


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


async def open_llama_with_printing(
    ctx: core.Context, manager: profiles.ProfileManager, offer: dict
) -> None:
    template_id = offer["itemGrants"][0]["templateId"].lower()
    llama_name = ctx.ast.get_item_str(template_id)

    ctx.log.message(
        ctx.ast.get_ui_str("llamas_cli.main.opening").format(llama_name), end=" "
    )

    loot_result = await llamas.purchase_xray_llama(manager, offer)

    ctx.log.message(ctx.ast.get_ui_str("llamas_cli.main.success"), hide_date_time=True)

    format_and_print_loot(ctx, loot_result)


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    if not ctx.cfg.global_config["open_free_llamas"]:
        return

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

    for offer in free_llama_offers:
        for _ in range(offer["num_left_to_buy"]):
            await open_llama_with_printing(ctx, manager, offer)
