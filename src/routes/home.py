"""Dashboard route — the wardrobe-at-a-glance landing page."""
from tina4_python.core.router import get
from tina4_python.swagger import description, tags
from src.orm.WardrobeItem import WardrobeItem
from src.app.outfit_engine import CATEGORIES
from src.app.auth_helpers import require_login, auth_context

CATEGORY_ICONS = {
    "top": "\U0001f455", "bottom": "\U0001f456", "dress": "\U0001f457",
    "shoes": "\U0001f45f", "jacket": "\U0001f9e5", "accessory": "\U0001f45c",
}

CATEGORY_LABELS = {
    "top": "Tops", "bottom": "Bottoms", "dress": "Dresses",
    "shoes": "Shoes", "jacket": "Jackets", "accessory": "Accessories",
}


@description("Render the dashboard: total item count, per-category breakdown, and the six most recently added items.")
@tags(["pages"])
@get("/")
async def home(request, response):
    """Render the wardrobe dashboard (HTML). Requires login."""
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    items = WardrobeItem.where("user_id = ?", params=[user_id], limit=500)
    counts = {c: 0 for c in CATEGORIES}
    for item in items:
        if item.category in counts:
            counts[item.category] += 1
    stat_cards = [
        {"category": c, "label": CATEGORY_LABELS[c],
         "count": counts[c], "icon": CATEGORY_ICONS[c]}
        for c in CATEGORIES
    ]
    recent = sorted(items, key=lambda i: i.id or 0, reverse=True)[:6]
    return response.render("dashboard.twig", {
        **auth_context(request),
        "nav_active": "home",
        "title": "Your Wardrobe at a Glance",
        "total": len(items),
        "stat_cards": stat_cards,
        "recent": [i.to_dict() for i in recent],
    })
