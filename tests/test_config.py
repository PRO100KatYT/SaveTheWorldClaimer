import config
import pathlib

GLOBAL_CONFIG_PATH = pathlib.Path(__file__).parent / "config.json"
USER_CONFIG_PATH = pathlib.Path(__file__).parent / "user_config.json"


def test_save_and_read_global_config():
    cfg = config.ConfigManager()

    content = {
        "test_option_1": True,
        "test_option_2": 1,
        "test_option_3": "man",
    }

    cfg.global_config.update(content)

    assert cfg.save_global_config(GLOBAL_CONFIG_PATH)

    cfg.load_global_config(GLOBAL_CONFIG_PATH)

    for option in content:
        assert cfg.global_config[option] == content[option]

    GLOBAL_CONFIG_PATH.unlink()


def test_save_and_read_user_config():
    cfg = config.ConfigManager()

    content = {
        "test_account_id_1": {
            "test_option_1": True,
            "test_option_2": 1,
            "test_option_3": "man",
        },
        "test_account_id_2": {"test_option_4": False},
    }

    cfg.user_config.update(content)

    assert cfg.save_user_config(USER_CONFIG_PATH)

    cfg.load_user_config(USER_CONFIG_PATH)

    for account_id in content:
        for option in content[account_id]:
            assert cfg.user_config[account_id][option] == content[account_id][option]

    USER_CONFIG_PATH.unlink()


def test_read_non_json_global_config_file():
    cfg = config.ConfigManager()

    with open(GLOBAL_CONFIG_PATH, "w") as file:
        file.write("e")

    cfg.load_global_config(GLOBAL_CONFIG_PATH)
    assert isinstance(cfg.global_config, dict)

    GLOBAL_CONFIG_PATH.unlink()


def test_read_non_json_user_config_file():
    cfg = config.ConfigManager()

    with open(USER_CONFIG_PATH, "w") as file:
        file.write("e")

    cfg.load_user_config(USER_CONFIG_PATH)
    assert isinstance(cfg.user_config, dict)

    USER_CONFIG_PATH.unlink()


def test_read_non_existing_global_config_file():
    cfg = config.ConfigManager()

    cfg.load_global_config(GLOBAL_CONFIG_PATH)
    assert isinstance(cfg.global_config, dict)

    GLOBAL_CONFIG_PATH.unlink()


def test_read_non_existing_user_config_file():
    cfg = config.ConfigManager()

    cfg.load_user_config(USER_CONFIG_PATH)
    assert isinstance(cfg.user_config, dict)

    USER_CONFIG_PATH.unlink()
