import json
from typing import Any

import importlib.metadata
from datetime import datetime
from zoneinfo import ZoneInfo

from .constants.iso_codes import ISO_CODES

TZ = ZoneInfo("Europe/Moscow")
__version__ = importlib.metadata.version("osm-ru-nametag-validator")

stats: dict[str, Any] = {
    "update_time": datetime.now(TZ).strftime("%d/%m/%Y %H:%M:%S"),
    "version": __version__.split(".dev")[0] + ".dev" if ".dev"
    in __version__ else __version__,

    "names_amount": {
        "all": 0,
        "legal": 0,
        "region": {item["name"]: 0 for item
                   in ISO_CODES}
    },

    "exceptions": {"amount": 0, "pct": 0},

    "variant": {
        i: {
            "amount": 0,
            "pct": 0,
            "region": {item["name"]: {"amount": 0, "pct": 0} for item
                       in ISO_CODES}
        }
        for i in range(1, 6)
    }
}


def _get_pcts() -> None:
    anames = stats["names_amount"]["all"]
    lnames = stats["names_amount"]["legal"]

    epct = round(stats["exceptions"]["amount"] / anames * 100) if anames else 0
    stats["exceptions"]["pct"] = epct

    for var in stats["variant"].values():
        var["pct"] = round(var["amount"] / lnames * 100) if lnames else 0

        for r in ISO_CODES:
            name = r["name"]
            areg_names = stats["names_amount"]["region"][name]
            reg_amount = var["region"][name]["amount"]

            rpct = round(reg_amount / areg_names * 100) if areg_names else 0
            var["region"][name]["pct"] = rpct


def _write_iso_codes(ISO_CODES_DATA: str, REGIONS_DATA: str) -> None:
    counts = stats["names_amount"]["region"]
    ISO_CODES.sort(key=lambda x: counts.get(x["name"], 0), reverse=True)

    with open(ISO_CODES_DATA, "w") as f:
        json.dump(ISO_CODES, f, ensure_ascii=False, indent=2)


def write_stats(
        STATS_FILE: str,
        ISO_CODES_DATA: str,
        REGIONS_DATA: str
) -> None:
    _write_iso_codes(ISO_CODES_DATA, REGIONS_DATA)
    _get_pcts()

    with open(STATS_FILE, 'w', encoding='utf-8') as fp:
        json.dump(stats, fp, ensure_ascii=False, indent=2)
