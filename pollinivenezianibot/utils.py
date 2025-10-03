import datetime
import logging
from functools import cmp_to_key

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
    else:
        return 1


def get_monday() -> datetime.date:
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday() + 8)


def get_dati_continui() -> dict:
    url = (
        "https://sdi.isprambiente.it/geoserver/om/ows?service=WFS&version=2.0.0"
        + "&request=GetFeature&typeName=om%3AConcentrazione_pollini_spore&cql_filter=STAT_ID=55&outputFormat=json"
    )
    response = requests.request("GET", url)
    out = {}
    for info in response.json()["features"]:
        e = info["properties"]
        if e["REMA_CONCENTRATION"] and e["REMA_CONCENTRATION"] > 0:
            out[e["PART_ID"]] = e["REMA_CONCENTRATION"]
    return out


def get_pollini() -> dict:
    url = (
        "https://sdi.isprambiente.it/geoserver/om/ows?service=WFS&version=2.0.0"
        + "&request=GetFeature&typeName=om%3APollini_spore&outputFormat=json"
    )
    response = requests.request("GET", url)
    out = {}
    for info in response.json()["features"]:
        e = info["properties"]
        idd = info["id"].split(".")[1]
        if e["PART_NAME_I"] and e["PART_HIGH"] and e["PART_HIGH"] > 0:
            out[int(idd)] = {
                "name": e["PART_NAME_I"],
                "levels": [e["PART_LOW"], e["PART_MIDDLE"], e["PART_HIGH"]],
            }
    return out


def get_level(limits: list, number: float = 0.0) -> tuple[str, str]:
    if number is None:
        number = 0.0
    if number < limits[0]:
        return "⚪", "None"
    if number < limits[1]:
        return "🟢", "Low"
    if number < limits[2]:
        return "🟠", "Medium"
    return "🔴", "High"


def get_printed_data() -> list[tuple[str, str, str]]:
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
    return out
