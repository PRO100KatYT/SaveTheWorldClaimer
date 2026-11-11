from features import inventory
import core
import profiles


async def assert_backpack_snapshot(
    ctx: core.Context, manager: profiles.ProfileManager
) -> None:
    backpack_snapshot = ctx.cfg.get_user_config(manager.mcp.account_id)[
        "inventory_junk_cleaner"
    ]["backpack_snapshot"]

    if not backpack_snapshot:
        await inventory.save_backpack_snapshot(ctx, manager)
        ctx.log.message(ctx.ast.get_ui_str("junk_cleaner_cli.snapshot_saved"))


async def recycle_and_destroy_items(
    ctx: core.Context, manager: profiles.ProfileManager, user_config: dict
) -> None:
    is_locked = await manager.is_profile_locked("theater0")
    if is_locked:
        ctx.log.message(ctx.ast.get_ui_str("junk_cleaner_cli.profile_locked"))
        return

    guids_to_recycle, guids_to_destroy = await inventory.search_for_items(
        ctx, manager, user_config
    )

    if guids_to_recycle:
        ctx.log.message(
            ctx.ast.get_ui_str("junk_cleaner_cli.recycling").format(
                len(guids_to_recycle),
                ctx.ast.get_plural_word("items", len(guids_to_recycle)),
            )
        )

        try:
            await manager.disassemble_world_items("theater0", guids_to_recycle)
        except ValueError:
            failed = 0
            for item in guids_to_recycle:
                try:
                    await manager.disassemble_world_items("theater0", [item])
                except ValueError:
                    guids_to_destroy.append(item["itemId"])
                    failed += 1

            if failed:
                ctx.log.message(
                    ctx.ast.get_ui_str("junk_cleaner_cli.recycling_failed").format(
                        failed,
                        ctx.ast.get_plural_word("items", len(guids_to_recycle)),
                    )
                )

    if guids_to_destroy:
        ctx.log.message(
            ctx.ast.get_ui_str("junk_cleaner_cli.destroying").format(
                len(guids_to_destroy),
                ctx.ast.get_plural_word("items", len(guids_to_destroy)),
            )
        )
        await manager.destroy_world_items("theater0", guids_to_destroy)


async def main(ctx: core.Context, manager: profiles.ProfileManager) -> None:
    user_config = ctx.cfg.get_user_config(manager.mcp.account_id)[
        "inventory_junk_cleaner"
    ]

    if not user_config["enabled"]:
        return

    await assert_backpack_snapshot(ctx, manager)
    await recycle_and_destroy_items(ctx, manager, user_config)
