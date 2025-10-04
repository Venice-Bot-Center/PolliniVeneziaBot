import datetime
import logging
from functools import cmp_to_key
from typing import List, Tuple

import requests
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def letter_cmp(a, b):
    if a[2] > b[2]:
        return -1
    if a[2] == b[2]:
        if a[0] > b[0]:
            return 1
        return -1
    return 1


def get_monday() -> datetime.date:
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday() + 8)


def get_dati_continui() -> dict:
    url = "http://dati.retecivica.bz.it/services/POLLNET_REMARKS"
    payload = {"format": "json", "STAT_ID": "55", "from": str(get_monday())}
    response = requests.request("GET", url, params=payload)
    out = {}
    for e in response.json():
        out[e["PART_ID"]] = e["REMA_CONCENTRATION"]
    return out


def get_pollini() -> dict:
    url = "http://dati.retecivica.bz.it/services/POLLNET_PARTICLES"
    payload = {"format": "json"}
    response = requests.request("GET", url, params=payload)
    out = {}
    for e in response.json():
        if e["PART_NAME_I"] and e["PART_HIGH"] and e["PART_HIGH"] > 0:
            out[e["PART_ID"]] = {
                "name": e["PART_NAME_I"],
                "levels": [e["PART_LOW"], e["PART_MIDDLE"], e["PART_HIGH"]],
            }
    return out


def get_level(limits: list, number: float = 0.0) -> (str, str):
    if number is None:
        number = 0.0
    if number < limits[0]:
        return "⚪", "None"
    if number < limits[1]:
        return "🟢", "Low"
    if number < limits[2]:
        return "🟠", "Medium"
    return "🔴", "High"


def get_printed_data() -> List[Tuple[str, str, str]]:
    dati = get_dati_continui()
    pollini = get_pollini()
    out = []
    for e in dati:
        try:
            pollin_data = pollini[e]
            pollin_level = dati[e]
            circle, str_level = get_level(
                number=pollin_level, limits=pollin_data["levels"]
            )
            name = pollin_data["name"]
            out.append((circle, str_level, name))
        except KeyError:
            pass
    letter_cmp_key = cmp_to_key(letter_cmp)
    out.sort(key=letter_cmp_key, reverse=True)
    log.debug(out)
    return out


def hashed(input_data: List[Tuple[str, str, str]]):
    out = ""
    for a, b, c in input_data:
        out += f"{a}{b}{c}"
    return out
