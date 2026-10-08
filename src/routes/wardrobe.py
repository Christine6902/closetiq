"""Wardrobe routes — the management page plus the add/delete JSON API."""
import base64
import os
import re
from datetime import datetime

from tina4_python.core.router import get, post, noauth
from tina4_python.swagger import description, tags
from src.orm.WardrobeItem import WardrobeItem
from src.app.outfit_engine import CATEGORIES, OCCASIONS

UPLOAD_DIR = "src/public/uploads"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


@description("Render the wardrobe grid. Pass ?category=<top|bottom|dress|shoes|jacket|accessory> to filter.")
@tags(["pages"])
@get("/wardrobe")
async def wardrobe_page(request, response):
    """Render the wardrobe management page (HTML), optionally filtered by category."""
    category = (request.query.get("category") or "").strip().lower()
    if category and category in CATEGORIES:
        items = WardrobeItem.where("category = ?", params=[category],
                                   limit=500, order_by="id DESC")
    else:
        category = ""
        items = WardrobeItem.all(limit=500, order_by="id DESC")
    return response.render("wardrobe.twig", {
        "nav_active": "wardrobe",
        "title": "My Wardrobe",
        "items": [i.to_dict() for i in items],
        "categories": CATEGORIES,
        "occasions": OCCASIONS,
        "active_category": category,
    })


@noauth()
@description("Create a wardrobe item. Accepts multipart form data: name, category, color, season, style_tags (comma-separated), and an optional image file. Returns the created item (201).")
@tags(["wardrobe"])
@post("/api/wardrobe")
async def add_item(request, response):
    """Create a wardrobe item from form data and return it as JSON (201)."""
    body = request.body or {}
    name = (body.get("name") or "").strip()
    category = (body.get("category") or "").strip().lower()
    if not name or category not in CATEGORIES:
        return response({"error": "A name and valid category are required."}, 400)

    tags = body.get("style_tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    image_url = _save_upload(request.files.get("image"))

    item = WardrobeItem({
        "name": name,
        "category": category,
        "color": (body.get("color") or "#94a3b8").strip(),
        "season": (body.get("season") or "all").strip().lower(),
        "style_tags": tags,
        "image_url": image_url,
        "times_worn": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    item.save()
    return response(item, 201)


@noauth()
@description("Delete the wardrobe item with the given id. Returns {deleted: id} or 404 if it does not exist.")
@tags(["wardrobe"])
@post("/api/wardrobe/{id:int}/delete")
async def delete_item(id, request, response):
    """Delete a wardrobe item by id; return {deleted: id} or 404."""
    item = WardrobeItem.find(id)
    if item is None:
        return response({"error": "Item not found."}, 404)
    item.delete()
    return response({"deleted": id})


def _save_upload(uploaded):
    """Persist an uploaded image to the public uploads dir; return its URL path."""
    if not uploaded:
        return ""
    if isinstance(uploaded, list):
        uploaded = uploaded[0] if uploaded else None
    if not uploaded or not uploaded.get("content"):
        return ""

    filename = uploaded.get("filename", "upload")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return ""

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", os.path.basename(filename))
    unique = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{safe}"
    with open(os.path.join(UPLOAD_DIR, unique), "wb") as fh:
        fh.write(base64.b64decode(uploaded["content"]))
    return f"/uploads/{unique}"
