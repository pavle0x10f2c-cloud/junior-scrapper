import json
import os

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
        "email": {
            "to": "",
            "from": "",
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587, #TLS
            "smtp_user": "",
            "smtp_password": ""
        },
        "schedule": {
            "time": "08:00" #system timezone
        },
        "keywords": [
            "junior", "noc", "cloud", "network engineer",
            "devops", "linux", "sysadmin", "system administrator",
            "it support", "helpdesk", "infrastructure"
        ]
}
def load_config() -> dict:
    if not os.path.exsists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(cfg: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2) #DEFAULT_CONFIG may have different spacing, will check
    print(f"[Config] Saved to {CONFIG_PATH}")

