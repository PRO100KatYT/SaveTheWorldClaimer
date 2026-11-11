import utils
from pathlib import Path
import json
from collections import defaultdict

GLOBAL_CONFIG_PATH: Path = utils.base_path(True) / "config.json"
USER_CONFIG_PATH: Path = utils.base_path(True) / "user_config.json"


GLOBAL_CONFIG_DATA = {
    "ui_language": {
        "display_name": "config.ui_language.display_name",
        "description": "config.ui_language.description",
        "type": str,
        "valid_values": ["en", "pl"],
        "default": "en",
    },
    "items_language": {
        "display_name": "config.items_language.display_name",
        "description": "config.items_language.description",
        "type": str,
        "valid_values": [
            "ar",
            "de",
            "en",
            "es-419",
            "es",
            "fr",
            "id",
            "it",
            "ja",
            "ko",
            "pl",
            "pt-BR",
            "ru",
            "th",
            "tr",
            "vi",
            "zh-Hans",
            "zh-Hant",
        ],
        "default": "en",
    },
    "open_free_llamas": {
        "display_name": "config.open_free_llamas.display_name",
        "description": "config.open_free_llamas.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
    "show_date_time": {
        "display_name": "config.show_date_time.display_name",
        "description": "config.show_date_time.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
    "discord_webhook_url": {
        "display_name": "config.discord_webhook_url.display_name",
        "description": "config.discord_webhook_url.description",
        "type": str,
        "valid_values": [],
        "default": "",
    },
    "check_for_updates": {
        "display_name": "config.check_for_updates.display_name",
        "description": "config.check_for_updates.description",
        "type": bool,
        "valid_values": [True, False],
        "default": True,
    },
}

USER_CONFIG_DATA = {
    "llama_loot_recycling": {
        "display_name": "config.llama_loot_recycling",
        "content": {
            "weapon": {
                "display_name": "config.recycle_weapons.display_name",
                "description": "config.recycle_weapons.description",
                "type": str,
                "valid_values": ["off", "common", "uncommon", "rare", "epic"],
                "default": "rare",
            },
            "trap": {
                "display_name": "config.recycle_traps.display_name",
                "description": "config.recycle_traps.description",
                "type": str,
                "valid_values": ["off", "common", "uncommon", "rare", "epic"],
                "default": "rare",
            },
            "survivor": {
                "display_name": "config.retire_survivors.display_name",
                "description": "config.retire_survivors.description",
                "type": str,
                "valid_values": ["off", "common", "uncommon", "rare", "epic"],
                "default": "epic",
            },
            "defender": {
                "display_name": "config.retire_defenders.display_name",
                "description": "config.retire_defenders.description",
                "type": str,
                "valid_values": ["off", "common", "uncommon", "rare", "epic"],
                "default": "epic",
            },
            "hero": {
                "display_name": "config.retire_heroes.display_name",
                "description": "config.retire_heroes.description",
                "type": str,
                "valid_values": ["off", "common", "uncommon", "rare", "epic"],
                "default": "rare",
            },
        },
    },
    "inventory_junk_cleaner": {
        "display_name": "config.inv_junk_cleaner",
        "content": {
            "backpack_snapshot": {
                "display_name": "config.inv_junk_cleaner.snapshot.display_name",
                "description": "config.inv_junk_cleaner.snapshot.description",
                "type": str,
                "valid_values": [],
                "default": "",
                "hidden": True,
            },
            "enabled": {
                "display_name": "config.inv_junk_cleaner.enabled.display_name",
                "description": "config.inv_junk_cleaner.enabled.description",
                "type": bool,
                "valid_values": [True, False],
                "default": False,
            },
            "tier": {
                "display_name": "config.inv_junk_cleaner.tier.display_name",
                "description": "config.inv_junk_cleaner.tier.description",
                "type": int,
                "valid_values": [2, 3, 4, 5],
                "default": 5,
            },
            "power_level": {
                "display_name": "config.inv_junk_cleaner.power_level.display_name",
                "description": "config.inv_junk_cleaner.power_level.description",
                "type": int,
                "valid_values": [],
                "default": 130,
            },
        },
    },
    "item_shop_purchaser": {
        "display_name": "config.item_shop_purchaser.display_name",
        "content": {
            "enabled": {
                "display_name": "config.item_shop_purchaser.enabled.display_name",
                "description": "config.item_shop_purchaser.enabled.description",
                "type": bool,
                "valid_values": [True, False],
                "default": False,
            },
            "evolution_materials": {
                "display_name": "config.item_shop_purchaser.evolution_materials.display_name",
                "content": {
                    "pure_drops_of_rain": {
                        "display_name": "config.item_shop_purchaser.pure_drops_of_rain.display_name",
                        "description": "config.item_shop_purchaser.pure_drops_of_rain.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_c_t01"]
                        },
                    },
                    "lightning_bottles": {
                        "display_name": "config.item_shop_purchaser.lightning_bottles.display_name",
                        "description": "config.item_shop_purchaser.lightning_bottles.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_c_t02"]
                        },
                    },
                    "eyes_of_the_storm": {
                        "display_name": "config.item_shop_purchaser.eyes_of_the_storm.display_name",
                        "description": "config.item_shop_purchaser.eyes_of_the_storm.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_c_t03"]
                        },
                    },
                    "storm_shards": {
                        "display_name": "config.item_shop_purchaser.storm_shards.display_name",
                        "description": "config.item_shop_purchaser.storm_shards.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_c_t04"]
                        },
                    },
                    "superchargers": {
                        "display_name": "config.item_shop_purchaser.superchargers.display_name",
                        "description": "config.item_shop_purchaser.superchargers.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_promotion_weapons",
                                "accountresource:reagent_promotion_heroes",
                                "accountresource:reagent_promotion_traps",
                                "accountresource:reagent_promotion_survivors",
                            ]
                        },
                    },
                },
            },
            "flux": {
                "display_name": "config.item_shop_purchaser.flux.display_name",
                "content": {
                    "legendary": {
                        "display_name": "config.item_shop_purchaser.legendary_flux.display_name",
                        "description": "config.item_shop_purchaser.legendary_flux.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_evolverarity_sr"]
                        },
                    },
                    "epic": {
                        "display_name": "config.item_shop_purchaser.epic_flux.display_name",
                        "description": "config.item_shop_purchaser.epic_flux.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_evolverarity_vr"]
                        },
                    },
                    "rare": {
                        "display_name": "config.item_shop_purchaser.rare_flux.display_name",
                        "description": "config.item_shop_purchaser.rare_flux.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": ["accountresource:reagent_evolverarity_r"]
                        },
                    },
                },
            },
            "perk_materials": {
                "display_name": "config.item_shop_purchaser.perk_materials.display_name",
                "content": {
                    "legendary": {
                        "display_name": "config.item_shop_purchaser.legendary_perkup.display_name",
                        "description": "config.item_shop_purchaser.legendary_perkup.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_alteration_upgrade_sr"
                            ]
                        },
                    },
                    "epic": {
                        "display_name": "config.item_shop_purchaser.epic_perkup.display_name",
                        "description": "config.item_shop_purchaser.epic_perkup.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_alteration_upgrade_vr"
                            ]
                        },
                    },
                    "rare": {
                        "display_name": "config.item_shop_purchaser.rare_perkup.display_name",
                        "description": "config.item_shop_purchaser.rare_perkup.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_alteration_upgrade_r"
                            ]
                        },
                    },
                    "uncommon": {
                        "display_name": "config.item_shop_purchaser.uncommon_perkup.display_name",
                        "description": "config.item_shop_purchaser.uncommon_perkup.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_alteration_upgrade_uc"
                            ]
                        },
                    },
                    "re_perk": {
                        "display_name": "config.item_shop_purchaser.re_perk.display_name",
                        "description": "config.item_shop_purchaser.re_perk.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": [
                                "accountresource:reagent_alteration_generic"
                            ]
                        },
                    },
                },
            },
            "survivors": {
                "display_name": "config.item_shop_purchaser.survivors.display_name",
                "content": {
                    "legendary": {
                        "display_name": "config.item_shop_purchaser.legendary_survivors.display_name",
                        "description": "config.item_shop_purchaser.legendary_survivors.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "starts_with": ["worker:"],
                            "contains": ["_sr_"],
                        },
                    },
                    "epic": {
                        "display_name": "config.item_shop_purchaser.epic_survivors.display_name",
                        "description": "config.item_shop_purchaser.epic_survivors.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "starts_with": ["worker:"],
                            "contains": ["_vr_"],
                        },
                    },
                },
            },
            "heroes": {
                "display_name": "config.item_shop_purchaser.heroes.display_name",
                "content": {
                    "mythic_and_legendary": {
                        "display_name": "config.item_shop_purchaser.mythic_and_legendary_heroes.display_name",
                        "description": "config.item_shop_purchaser.mythic_and_legendary_heroes.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "starts_with": ["hero:"],
                            "contains": ["_sr_"],
                        },
                    },
                    "epic": {
                        "display_name": "config.item_shop_purchaser.epic_heroes.display_name",
                        "description": "config.item_shop_purchaser.epic_heroes.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "starts_with": ["hero:"],
                            "contains": ["_vr_"],
                        },
                    },
                },
            },
            "schematics": {
                "display_name": "config.item_shop_purchaser.schematics.display_name",
                "content": {
                    "legendary": {
                        "display_name": "config.item_shop_purchaser.legendary_schematics.display_name",
                        "description": "config.item_shop_purchaser.legendary_schematics.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "starts_with": ["schematic:"],
                            "contains": ["_sr_"],
                        },
                    },
                    "epic": {
                        "display_name": "config.item_shop_purchaser.epic_schematics.display_name",
                        "description": "config.item_shop_purchaser.epic_schematics.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "starts_with": ["schematic:"],
                            "contains": ["_vr_"],
                        },
                    },
                },
            },
            "defenders": {
                "display_name": "config.item_shop_purchaser.defenders.display_name",
                "content": {
                    "legendary": {
                        "display_name": "config.item_shop_purchaser.legendary_defenders.display_name",
                        "description": "config.item_shop_purchaser.legendary_defenders.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "starts_with": ["defender:"],
                            "contains": ["_sr_"],
                        },
                    },
                },
            },
            "slots": {
                "display_name": "config.item_shop_purchaser.slots.display_name",
                "content": {
                    "armory": {
                        "display_name": "config.item_shop_purchaser.armory_slots.display_name",
                        "description": "config.item_shop_purchaser.armory_slots.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": True,
                        "eligible_shop_items": {
                            "template_ids": ["token:accountinventorybonus"]
                        },
                    },
                    "hero_loadout": {
                        "display_name": "config.item_shop_purchaser.hero_loadouts.display_name",
                        "description": "config.item_shop_purchaser.hero_loadouts.description",
                        "type": bool,
                        "valid_values": [True, False],
                        "default": False,
                        "eligible_shop_items": {
                            "template_ids": [
                                "campaignheroloadout:purchaseabledefaultloadout"
                            ]
                        },
                    },
                },
            },
            "gold": {
                "display_name": "config.item_shop_purchaser.gold.display_name",
                "content": {
                    "dont_spend_below": {
                        "display_name": "config.item_shop_purchaser.dont_spend_below_gold.display_name",
                        "description": "config.item_shop_purchaser.dont_spend_below_gold.description",
                        "type": int,
                        "valid_values": [],
                        "default": 5000,
                    },
                },
            },
        },
    },
}


class ConfigManager:
    def __init__(self):
        self.global_config = self.get_default_global_config()
        self.user_config = defaultdict(dict)
        self._listeners = defaultdict(list)

        self.load_global_config()
        self.load_user_config()

    def get_default_global_config(self) -> dict:
        global_config = {}

        for option in GLOBAL_CONFIG_DATA:
            global_config[option] = GLOBAL_CONFIG_DATA[option]["default"]

        return global_config

    def get_user_config(self, account_id: str) -> dict:
        def crawl(data_part: dict, config_part: dict) -> None:
            for key in data_part:
                if "type" in data_part[key]:
                    if key not in config_part:
                        config_part[key] = data_part[key]["default"]
                else:
                    if key not in config_part:
                        config_part[key] = {}

                    if "content" in data_part[key]:
                        crawl(data_part[key]["content"], config_part[key])

        crawl(USER_CONFIG_DATA, self.user_config[account_id])

        self.save_user_config()
        return self.user_config[account_id]

    def save_config(self, path: Path, config: dict) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(config, file, indent=2, ensure_ascii=False)
                return True
        except PermissionError:
            return False

    def save_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> bool:
        return self.save_config(path, self.global_config)

    def save_user_config(self, path: Path = USER_CONFIG_PATH) -> bool:
        return self.save_config(path, self.user_config)

    def load_config(self, path: Path, destination: dict, save_function) -> None:
        try:
            with open(path, "r", encoding="utf-8") as file:
                destination.update(json.load(file))
        except FileNotFoundError:
            save_function(path)
        except json.JSONDecodeError:
            path.unlink()
            save_function(path)

    def load_global_config(self, path: Path = GLOBAL_CONFIG_PATH) -> None:
        self.load_config(path, self.global_config, self.save_global_config)

    def load_user_config(self, path: Path = USER_CONFIG_PATH) -> None:
        self.load_config(path, self.user_config, self.save_user_config)

    def add_listener(self, option: str, function) -> None:
        self._listeners[option].append(function)

    def notify_listeners(self, option: str) -> None:
        functions = self._listeners.get(option, [])

        for function in functions:
            function(self.global_config[option])

    def set_global_value(self, option: str, value) -> None:
        if self.global_config[option] == value:
            return

        self.global_config[option] = value
        self.save_global_config()
        self.notify_listeners(option)

    def set_user_value(self, account_id: str, path: list, value) -> None:
        config_part = self.user_config[account_id]

        for i in range(len(path) - 1):
            config_part = config_part[path[i]]

        config_part[path[-1]] = value

        self.save_user_config()
