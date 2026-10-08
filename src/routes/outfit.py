"""Outfit route — the 'Today's Look' generator page."""
from tina4_python.core.router import get
from tina4_python.swagger import description, tags
from src.orm.WardrobeItem import WardrobeItem
from src.app.outfit_engine import generate_outfit, OCCASIONS, WEATHER

# Display order of the slots in a generated outfit.
SLOT_ORDER = ["dress", "top", "bottom", "jacket", "shoes", "accessory"]


@description("Generate and render a coordinated outfit. Query params: occasion (casual|smart-casual|corporate|formal|date|sport) and weather (hot|mild|cold|rainy).")
@tags(["pages"])
@get("/outfit")
async def outfit_page(request, response):
    """Render a generated outfit (HTML) for the chosen occasion and weather."""
    occasion = (request.query.get("occasion") or "").strip().lower()
    weather = (request.query.get("weather") or "mild").strip().lower()
    if occasion not in OCCASIONS:
        occasion = ""
    if weather not in WEATHER:
        weather = "mild"

    items = WardrobeItem.all(limit=500)
    outfit = generate_outfit(items, occasion=occasion or None, weather=weather)
    pieces = [dict(item.to_dict(), slot=slot)
              for slot in SLOT_ORDER if slot in outfit
              for item in [outfit[slot]]]

    return response.render("outfit.twig", {
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
