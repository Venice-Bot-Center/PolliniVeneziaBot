import logging

from rich.logging import RichHandler

from pollinivenezianibot.telegram_api import telegram_send
from pollinivenezianibot.utils import get_printed_data

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def main():
    telegram_send("Hello from polliniveneziabot!")
    logging.info(get_printed_data())


if __name__ == "__main__":
    main()
