"""Wardrobe routes — the management page plus the add/delete JSON API."""
import base64
import os
import re
from datetime import datetime

from tina4_python.core.router import get, post
from tina4_python.swagger import description, tags
from src.orm.WardrobeItem import WardrobeItem
from src.app.outfit_engine import CATEGORIES, OCCASIONS
from src.app.auth_helpers import require_login, auth_context

UPLOAD_DIR = "src/public/uploads"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


@description("Render the wardrobe grid. Pass ?category= to filter.")
@tags(["pages"])
@get("/wardrobe")
async def wardrobe_page(request, response):
    """Render the wardrobe management page (HTML). Requires login."""
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    category = (request.query.get("category") or "").strip().lower()
    if category and category in CATEGORIES:
        items = WardrobeItem.where("user_id = ? AND category = ?",
                                   params=[user_id, category],
                                   limit=500, order_by="id DESC")
    else:
        category = ""
        items = WardrobeItem.where("user_id = ?", params=[user_id],
                                   limit=500, order_by="id DESC")
    return response.render("wardrobe.twig", {
        **auth_context(request),
        "nav_active": "wardrobe",
        "title": "My Wardrobe",
        "items": [i.to_dict() for i in items],
        "categories": CATEGORIES,
        "occasions": OCCASIONS,
        "active_category": category,
    })


@description("Create a wardrobe item for the logged-in user. Accepts multipart form data.")
@tags(["wardrobe"])
@post("/api/wardrobe")
async def add_item(request, response):
    """Create a wardrobe item owned by the session user. Returns 201."""
    user_id, redirect = require_login(request, response)
    if redirect:
        return response({"error": "Not authenticated"}, 401)

    body = request.body or {}
    name = (body.get("name") or "").strip()
    category = (body.get("category") or "").strip().lower()
    if not name or category not in CATEGORIES:
        return response({"error": "A name and valid category are required."}, 400)

    item_tags = body.get("style_tags") or []
    if isinstance(item_tags, str):
        item_tags = [t.strip() for t in item_tags.split(",") if t.strip()]

    image_url = _save_upload(request.files.get("image"))

    item = WardrobeItem({
        "name": name,
        "category": category,
        "color": (body.get("color") or "#94a3b8").strip(),
        "season": (body.get("season") or "all").strip().lower(),
        "style_tags": item_tags,
        "image_url": image_url,
        "user_id": user_id,
        "times_worn": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    item.save()
    return response(item, 201)


@description("Delete a wardrobe item. Only the owner can delete.")
@tags(["wardrobe"])
@post("/api/wardrobe/{id:int}/delete")
async def delete_item(id, request, response):
    """Delete a wardrobe item by id — only if it belongs to the session user."""
    user_id, redirect = require_login(request, response)
    if redirect:
        return response({"error": "Not authenticated"}, 401)

    item = WardrobeItem.find(id)
    if item is None:
        return response({"error": "Item not found."}, 404)
    if item.user_id != user_id:
        return response({"error": "Not your item."}, 403)
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
