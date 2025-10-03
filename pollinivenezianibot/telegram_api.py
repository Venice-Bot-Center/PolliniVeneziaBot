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


def telegram_send(text: str) -> tuple[int, bool] | tuple[None, bool]:

    logging.info(TOKEN)
    logging.info(CHANNEL)

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHANNEL}&text={text}"
    r = requests.get(url=url)
    logging.info(r.json())
    if r.json()["ok"]:
        return r.json()["result"]["message_id"], True
    return None, False
