import core
import profiles
from features import item_shop


def print_purchase_info(ctx: core.Context, offer: dict, purchase_quantity: int) -> None:
    for item in offer["itemGrants"]:
        template_id = item["templateId"].lower()
        quantity = purchase_quantity * item["quantity"]
        name = ctx.ast.get_item_str(template_id)
        item_data = ctx.ast.get_item_data(template_id)
        rarity = ctx.ast.get_rarity_str(item_data.get("rarity", "???"))
        color = ctx.ast.get_rarity_color(rarity)
        item_type = ctx.ast.get_type_str(item_data.get("type", "???"))

        ctx.log.message(
            ctx.ast.get_ui_str("item_shop_cli.purchased").format(
                rarity, item_type, quantity, name, color
            )
        )


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    user_config = ctx.cfg.get_user_config(manager.mcp.account_id)["item_shop_purchaser"]

    if not user_config["enabled"]:
        return

    initial_gold = await item_shop.get_gold_quantity(manager)

    offers = await item_shop.get_catalog_offers_to_purchase(manager, user_config)
    for offer in offers:
        purchase_quantity = await item_shop.get_affordable_purchase_quantity(
            manager, offer, user_config
        )

        if purchase_quantity <= 0:
            continue

        await item_shop.purchase_catalog_offer(manager, offer, purchase_quantity)

        print_purchase_info(ctx, offer, purchase_quantity)

    current_gold = await item_shop.get_gold_quantity(manager)
    gold_diff = initial_gold - current_gold

    if gold_diff > 0:
        ctx.log.message(
            ctx.ast.get_ui_str("item_shop_cli.goldspent").format(
                gold_diff, current_gold
            )
        )
