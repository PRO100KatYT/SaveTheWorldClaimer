import profiles
import pathlib
import json
import pytest
import api


@pytest.fixture
def get_test_manager():
    profile_path = (
        pathlib.Path(__file__).parent / "jsons" / "profiles" / "campaign.json"
    )
    with open(profile_path, "r") as file:
        profile = json.load(file)

    epic_api = api.EpicAPI()
    mcp_api = api.McpAPI("test_account_id", epic_api)
    manager = profiles.ProfileManager(mcp_api)
    manager.cache = {"campaign": profile}
    return manager


def test_profile_changes_itemadded(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "itemAdded",
            "enableConstructDelta": True,
            "itemId": "7937cd58-b618-4d7a-9f1c-edeea58208e4",
            "item": {
                "templateId": "CardPack:zcp_tutorial_ranged",
                "attributes": {
                    "match_statistics": {
                        "mission_name": "OB_FarmsteadFort",
                        "total_seconds_in_match": 616,
                        "matchmaking_session_id": "eb0007d2fbba4e63a9871476971b4d13",
                        "eligibility_status": "User",
                    },
                    "level": 15,
                    "pack_source": "Mission:15",
                },
                "quantity": 1,
            },
        },
        {
            "changeType": "itemAdded",
            "enableConstructDelta": True,
            "itemId": "7546b312-8e3b-4ec2-ae98-7cb1945237a1",
            "item": {
                "templateId": "Quest:achievement_playwithothers",
                "attributes": {
                    "creation_time": "2023-04-08T17:10:32.197Z",
                    "quest_state": "Active",
                    "last_state_change_time": "2023-04-08T17:10:32.197Z",
                    "level": -1,
                    "quest_rarity": "uncommon",
                    "xp_reward_scalar": 1,
                },
                "quantity": 1,
            },
        },
        {
            "changeType": "itemAdded",
            "enableConstructDelta": True,
            "itemId": "ae34705d-f0dc-4c72-8e95-7cb3f6408e9c",
            "item": {
                "templateId": "Schematic:sid_floor_spikes_wood_c_t01",
                "attributes": {
                    "level": 1,
                    "alterations": [
                        "Alteration:aid_att_damage_physical_t02",
                        "Alteration:aid_att_maxdurability_trap_t02",
                        "Alteration:aid_att_damage_t02",
                        "Alteration:aid_att_maxdurability_trap_t02",
                        "Alteration:aid_att_maxdurability_trap_t03",
                        "Alteration:aid_att_maxdurability_trap_t03",
                    ],
                },
                "quantity": 1,
            },
        },
    ]

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        item_id, item = entry["itemId"], entry["item"]

        assert manager.cache["campaign"]["items"][item_id] == item


def test_profile_changes_itemremoved(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "itemRemoved",
            "enableConstructDelta": True,
            "itemId": "f30bcacb-2210-4f9f-be92-b2d016e093e4",
        },
        {
            "changeType": "itemRemoved",
            "enableConstructDelta": True,
            "itemId": "7937cd58-b618-4d7a-9f1c-edeea58208e4",
        },
        {
            "changeType": "itemRemoved",
            "enableConstructDelta": True,
            "itemId": "74ea22bc-af13-4bf4-a4e4-f46fac511894",
        },
    ]

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        item_id = entry["itemId"]

        assert item_id not in manager.cache["campaign"]["items"]


def test_profile_changes_itemattrchanged(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "itemAttrChanged",
            "enableConstructDelta": True,
            "itemId": "09cf107f-38cf-4b27-b4a7-67cf696e65cf",
            "attributeName": "completion_stonewoodquest_hidden_hasitems",
            "attributeValue": 10,
            "oldValue": 7,
        },
        {
            "changeType": "itemAttrChanged",
            "enableConstructDelta": True,
            "itemId": "2bae0f60-4b6c-4328-af4b-54dacf90d4a3",
            "attributeName": "quest_state",
            "attributeValue": "Completed",
            "oldValue": "Active",
        },
    ]

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        item = manager.cache["campaign"]["items"][entry["itemId"]]

        assert item["attributes"][entry["attributeName"]] == entry["attributeValue"]


def test_profile_changes_itemquantitychanged(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "itemQuantityChanged",
            "enableConstructDelta": True,
            "itemId": "2a698f24-2c45-4a74-8de8-265cd0ee9b8f",
            "quantity": 123570,
            "oldQuantity": 113820,
        }
    ]

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        item = manager.cache["campaign"]["items"][entry["itemId"]]

        assert item["quantity"] == entry["quantity"]


def test_profile_changes_statmodified(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "statModified",
            "enableConstructDelta": True,
            "name": "quest_manager",
            "value": {
                "dailyLoginInterval": "2023-04-08T16:58:53.814Z",
                "dailyQuestRerolls": 1,
                "objectiveDeferral": {
                    "key": "c2031f0356f549e5bff852e732e9a729",
                    "instigationTime": "2023-04-08T17:12:09.091Z",
                },
            },
        },
        {
            "changeType": "statModified",
            "enableConstructDelta": True,
            "name": "gameplay_stats",
            "value": [{"statName": "zonescompleted", "statValue": 2}],
        },
    ]

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        stats = manager.cache["campaign"]["stats"]["attributes"]

        assert entry["name"] in stats
        assert stats[entry["name"]] == entry["value"]


def test_profile_changes_fullprofileupdate(get_test_manager):
    manager = get_test_manager

    profile_changes = [
        {
            "changeType": "fullProfileUpdate",
            "enableConstructDelta": True,
            "profile": {},
        }
    ]

    profile2_path = (
        pathlib.Path(__file__).parent / "jsons" / "profiles" / "campaign2.json"
    )
    with open(profile2_path, "r") as file:
        profile_changes[0]["profile"] = json.load(file)

    manager.process_profile_changes(profile_changes, "campaign")

    for entry in profile_changes:
        assert entry["profile"] == manager.cache["campaign"]


def test_get_profile_rvn(get_test_manager):
    manager = get_test_manager
    manager.cache["athena"] = {"commandRevision": 2136}

    assert manager.get_profile_rvn("athena") == 2136
    assert manager.get_profile_rvn("theater0") == -1


def test_update_revisions_headers(get_test_manager):
    manager = get_test_manager
    manager.cache["athena"] = {"commandRevision": 2136}

    manager.update_revisions_headers()

    for entry in json.loads(
        manager.mcp.epic.session.headers["X-EpicGames-ProfileRevisions"]
    ):
        assert (
            manager.cache[entry["profileId"]]["commandRevision"]
            == entry["clientCommandRevision"]
        )
