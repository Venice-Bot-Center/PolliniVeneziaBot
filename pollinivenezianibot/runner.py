import logging

from rich.logging import RichHandler

from pollinivenezianibot.db_istance import DBIstance
from pollinivenezianibot.telegram_api import telegram_channel_delete_message
from pollinivenezianibot.telegram_api import telegram_channel_send
from pollinivenezianibot.utils import get_printed_data
from pollinivenezianibot.utils import hashed

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def sender_message():
    data = get_printed_data()
    message = ""
    for a, b, c in data:
        if b != "None":
            message += f"{a} {c}\n"
    return telegram_channel_send(message)[0]


def run():
    db = DBIstance()
    data = get_printed_data()
    new_hash = hashed(data)
    if new_hash != db.pollini_hash:
        db.pollini_hash = new_hash
        if not telegram_channel_delete_message(message_id=db.pollini_mex):
            log.error("Problemi con la cancellazione")
        db.pollini_mex = sender_message()
