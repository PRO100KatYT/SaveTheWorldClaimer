from features import llamas
import core
import profiles


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
            loot_result = await llamas.purchase_xray_llama(manager, offer)
