import core
import profiles


async def get_free_llamas(manager: profiles.ProfileManager) -> list:
    catalog = await manager.mcp.get_catalog()

    xray_storefront = {}
    for storefront in catalog["storefronts"]:
        if storefront["name"].lower() == "cardpackstorepreroll":
            xray_storefront = storefront
            break

    if not xray_storefront:
        return []

    offers = []
    for entry in xray_storefront["catalogEntries"]:
        if not entry["prices"][0]["finalPrice"] == 0:
            continue

        if "always" in entry["devName"].lower():
            continue

        offers.append(entry)

    return offers
