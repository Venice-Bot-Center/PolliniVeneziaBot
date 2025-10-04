import logging

from rich.logging import RichHandler

from pollinivenezianibot.telegram_api import sender_message

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def main():
    logging.info(sender_message())


if __name__ == "__main__":
    main()
