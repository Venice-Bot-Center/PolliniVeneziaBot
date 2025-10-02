import logging
import os

import requests
from rich.logging import RichHandler

TOKEN = os.environ.get("TELEGRAM_KEY", "")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL", "")
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def telegram_send(text: str, user: str) -> tuple[int, bool] | tuple[None, bool]:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    message = {
        "chat_id": user,
        "text": text,
        "parse_mode": "Markdown",
    }
    r = requests.post(url=url, json=message)
    print(r.json())
    if r.json()["ok"]:
        return r.json()["result"]["message_id"], True
    return None, False


def telegram_channel_send(text: str) -> tuple[int, bool]:
    return telegram_send(text, CHANNEL)


def telegram_channel_delete_message(message_id: int, chat: str = CHANNEL) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    message = {"chat_id": chat, "message_id": message_id}
    r = requests.get(url=url, json=message)
    log.info(r.json())
    if r.json()["ok"]:
        return True
    else:
        return False
