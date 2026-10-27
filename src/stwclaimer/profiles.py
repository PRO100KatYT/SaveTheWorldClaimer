import api
import json


class ProfileManager:
    def __init__(self, mcp_api: api.McpAPI):
        self.mcp = mcp_api
        self.cache = {}

    async def get_profile(self, profile_id: str) -> dict:
        if profile_id not in self.cache:
            await self.query_profile(profile_id)
        return self.cache[profile_id]

    async def search_items(
        self,
        profile_id: str,
        template_id_lower: str,
        required_attributes: dict | None = None,
    ) -> list:
        profile = await self.get_profile(profile_id)

        guids = []
        for key in profile.get("items", {}):
            item = profile["items"][key]

            if item["templateId"].lower() != template_id_lower:
                continue

            if required_attributes:
                correct_attributes = 0
                for attribute in required_attributes:
                    if attribute not in item["attributes"]:
                        continue

                    if required_attributes[attribute] == any or str(
                        item["attributes"][attribute]
                    ).lower() == str(required_attributes[attribute]):
                        correct_attributes += 1

                if correct_attributes != len(required_attributes):
                    continue

            guids.append(key)

        return guids

    def get_item_template_id(self, profile: dict, guid: str) -> str:
        return profile["items"].get(guid, {"templateId": guid}).get("templateId")

    def get_profile_rvn(self, profile_id: str) -> int:
        if profile_id not in self.cache:
            self.cache[profile_id] = {"commandRevision": -1}
        return self.cache[profile_id]["commandRevision"]

    def set_revisions_headers(self) -> None:
        revisions = []

        for profile_id in self.cache:
            revisions.append(
                {
                    "profileId": profile_id,
                    "clientCommandRevision": self.cache[profile_id]["commandRevision"],
                }
            )

        headers = {
            "X-EpicGames-ProfileRevisions": json.dumps(revisions, separators=(",", ":"))
        }

        self.mcp.epic.session.headers.update(headers)

    def update_profile_revisions(self, profile_updates: dict, profile_id: str) -> None:
        profile_update = profile_updates[profile_id]
        profile = self.cache[profile_id]

        profile["rvn"] = profile_update["profileRevision"]
        profile["commandRevision"] = profile_update["profileCommandRevision"]

    def process_profile_changes(self, profile_changes: list, profile_id: str) -> None:
        for entry in profile_changes:
            match entry["changeType"]:
                case "itemAdded":
                    self.cache[profile_id]["items"][entry["itemId"]] = entry["item"]

                case "itemRemoved":
                    del self.cache[profile_id]["items"][entry["itemId"]]

                case "itemAttrChanged":
                    self.cache[profile_id]["items"][entry["itemId"]]["attributes"][
                        entry["attributeName"]
                    ] = entry["attributeValue"]

                case "itemQuantityChanged":
                    self.cache[profile_id]["items"][entry["itemId"]]["quantity"] = (
                        entry["quantity"]
                    )

                case "statModified":
                    self.cache[profile_id]["stats"]["attributes"][entry["name"]] = (
                        entry["value"]
                    )

                case "fullProfileUpdate":
                    self.cache[profile_id] = entry["profile"]

    def get_profile_changes(self, profile_updates: dict, profile_id: str) -> list:
        return profile_updates.get(profile_id, {}).get("profileChanges", [])

    async def base_request(
        self, operation: str, profile_id: str, json_body: dict = {}
    ) -> dict:
        rvn = self.get_profile_rvn(profile_id)
        self.set_revisions_headers()

        res = await self.mcp.client_request(operation, profile_id, rvn, json_body)

        profile_updates = {}

        if "multiUpdate" in res:
            for entry in res["multiUpdate"]:
                profile_updates[entry["profileId"]] = entry
            del res["multiUpdate"]

        profile_updates[res["profileId"]] = res

        for res_profile_id in profile_updates:
            profile_changes = self.get_profile_changes(profile_updates, res_profile_id)

            self.process_profile_changes(profile_changes, res_profile_id)

            self.update_profile_revisions(profile_updates, res_profile_id)

        return profile_updates

    async def query_profile(self, profile_id: str) -> dict:
        return await self.base_request("QueryProfile", profile_id)

    async def client_quest_login(self, profile_id: str) -> dict:
        return await self.base_request("ClientQuestLogin", profile_id)

    async def fort_reroll_daily_quest(self, profile_id: str, quest_id: str) -> dict:
        return await self.base_request(
            "FortRerollDailyQuest", profile_id, {"questId": quest_id}
        )

    async def populate_prerolled_offers(self, profile_id: str) -> dict:
        return await self.base_request("PopulatePrerolledOffers", profile_id)

    async def purchase_catalog_entry(
        self,
        profile_id: str,
        offer_id: str,
        purchase_quantity: int,
        currency: str,
        currency_subtype: str,
        expected_total_price: int,
    ) -> dict:
        return await self.base_request(
            "PurchaseCatalogEntry",
            profile_id,
            json_body={
                "offerId": offer_id,
                "purchaseQuantity": purchase_quantity,
                "currency": currency,
                "currencySubType": currency_subtype,
                "expectedTotalPrice": expected_total_price,
                "gameContext": "fn",
            },
        )

    async def recycle_item_batch(self, profile_id: str, target_item_ids: list) -> dict:
        return await self.base_request(
            "RecycleItemBatch", profile_id, {"targetItemIds": target_item_ids}
        )
