"""Outfit route — the 'Today's Look' generator page."""
from tina4_python.core.router import get
from tina4_python.swagger import description, tags
from src.orm.WardrobeItem import WardrobeItem
from src.app.outfit_engine import generate_outfit, OCCASIONS, WEATHER
from src.app.auth_helpers import require_login, auth_context

SLOT_ORDER = ["dress", "top", "bottom", "jacket", "shoes", "accessory"]


@description("Generate and render a coordinated outfit from the user's wardrobe.")
@tags(["pages"])
@get("/outfit")
async def outfit_page(request, response):
    """Render a generated outfit (HTML). Requires login."""
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    occasion = (request.query.get("occasion") or "").strip().lower()
    weather = (request.query.get("weather") or "mild").strip().lower()
    if occasion not in OCCASIONS:
        occasion = ""
    if weather not in WEATHER:
        weather = "mild"

    items = WardrobeItem.where("user_id = ?", params=[user_id], limit=500)
    outfit = generate_outfit(items, occasion=occasion or None, weather=weather)
    pieces = [dict(item.to_dict(), slot=slot)
              for slot in SLOT_ORDER if slot in outfit
              for item in [outfit[slot]]]

    return response.render("outfit.twig", {
        **auth_context(request),
        "nav_active": "outfit",
        "title": "Today's Look",
        "pieces": pieces,
        "occasions": OCCASIONS,
        "weather_options": [{"key": k, **v} for k, v in WEATHER.items()],
        "active_occasion": occasion,
        "active_weather": weather,
        "empty": len(pieces) == 0,
        "wardrobe_empty": len(items) == 0,
    })
