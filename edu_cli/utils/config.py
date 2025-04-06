"""
Configuration utilities for the Education CLI.
"""
import os
import json
import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".edu_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)

    # Create config file if it doesn't exist
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"api_key": None}, f)

    # Create history file if it doesn't exist
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)

def get_api_key():
    """Get the API key from the configuration file or environment."""
    # First check environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # Then check config file
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get("api_key")
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def save_api_key(api_key):
    """Save the API key to the configuration file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {}

    config["api_key"] = api_key

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def save_to_history(subject, topic, question, response):
    """Save an interaction to the history file."""
    ensure_config_dir()
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        history = []

    history.append({
        "subject": subject,
        "topic": topic,
        "question": question,
        "response": response,
        "timestamp": str(datetime.datetime.now())
    })

    # Keep only the last 100 entries
    if len(history) > 100:
        history = history[-100:]

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def get_history(limit=10):
    """Get the interaction history."""
    ensure_config_dir()
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
            return history[-limit:] if limit else history
    except (json.JSONDecodeError, FileNotFoundError):
        return []
