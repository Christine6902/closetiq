"""Outfit recommendation logic for ClosetIQ.

Combines wardrobe items into a coordinated look, filtered by occasion and
weather, favouring less-worn pieces so the whole wardrobe gets used.
"""
import random

CATEGORIES = ["top", "bottom", "dress", "shoes", "jacket", "accessory"]

OCCASIONS = ["casual", "smart-casual", "corporate", "formal", "date", "sport"]

WEATHER = {
    "hot":   {"label": "Hot",   "icon": "☀️", "exclude_season": "winter", "needs_jacket": False},
    "mild":  {"label": "Mild",  "icon": "⛅",       "exclude_season": None,     "needs_jacket": False},
    "cold":  {"label": "Cold",  "icon": "❄️", "exclude_season": "summer", "needs_jacket": True},
    "rainy": {"label": "Rainy", "icon": "\U0001f327️", "exclude_season": "summer", "needs_jacket": True},
}


def _matches(item, occasion, exclude_season):
    tags = item.style_tags or []
    if occasion and occasion not in tags:
        return False
    if exclude_season and item.season == exclude_season:
        return False
    return True


def _pick(pool):
    """Pick a piece, biased toward the least-worn items for wardrobe variety."""
    if not pool:
        return None
    ranked = sorted(pool, key=lambda i: i.times_worn or 0)
    tier = max(1, len(ranked) // 3)
    return random.choice(ranked[:tier])


def generate_outfit(items, occasion=None, weather="mild"):
    """Return a dict of {slot: WardrobeItem} for one coordinated outfit.

    Returns an empty dict if the wardrobe can't cover a minimal look.
    """
    weather_cfg = WEATHER.get(weather, WEATHER["mild"])
    exclude_season = weather_cfg["exclude_season"]

    pool = [i for i in items if _matches(i, occasion, exclude_season)]
    by_cat = {c: [i for i in pool if i.category == c] for c in CATEGORIES}

    outfit = {}
    # Base layer: a dress, or a top + bottom pairing.
    use_dress = bool(by_cat["dress"]) and (not by_cat["top"] or not by_cat["bottom"] or random.random() < 0.4)
    if use_dress:
        outfit["dress"] = _pick(by_cat["dress"])
    else:
        outfit["top"] = _pick(by_cat["top"])
        outfit["bottom"] = _pick(by_cat["bottom"])

    outfit["shoes"] = _pick(by_cat["shoes"])
    if weather_cfg["needs_jacket"]:
        outfit["jacket"] = _pick(by_cat["jacket"])
    outfit["accessory"] = _pick(by_cat["accessory"])

    outfit = {slot: item for slot, item in outfit.items() if item}

    # A usable look needs at least a base + shoes.
    has_base = "dress" in outfit or ("top" in outfit and "bottom" in outfit)
    if not (has_base and "shoes" in outfit):
        return {}
    return outfit
