import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path.home() / ".shulkerbox"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_default_config() -> Dict[str, Any]:
    """
    Returns the default configuration for ShulkerBox.
    """
    return {
        "shared_folder_path": str(Path.home() / "ShulkerBox"),
        "port": 8765,
        "start_on_login": False,
        "webdav_username": "",
        "webdav_password": ""
    }

def load_config() -> Dict[str, Any]:
    """
    Loads the configuration from the local JSON file.
    Merges with defaults if keys are missing.
    """
    defaults = get_default_config()

    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_config(defaults)
        return defaults

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Merge with defaults to handle missing keys in old versions
            return {**defaults, **config}
    except (json.JSONDecodeError, IOError):
        return defaults

def save_config(config: Dict[str, Any]) -> None:
    """
    Saves the provided configuration to the local JSON file.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
