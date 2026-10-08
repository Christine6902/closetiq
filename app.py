from tina4_python.core import run
from tina4_python.core.server import asgi
from tina4_python.frond import Frond

# ── Template globals ──────────────────────────────────────────────
Frond.add_global("APP_NAME", "ClosetIQ")

_CATEGORY_ICONS = {
    "top": "\U0001f455", "bottom": "\U0001f456", "dress": "\U0001f457",
    "shoes": "\U0001f45f", "jacket": "\U0001f9e5", "accessory": "\U0001f45c",
}
Frond.add_global("category_icon", lambda category: _CATEGORY_ICONS.get(category, "\U0001f9f5"))

# The ASGI application. Point any ASGI server at it:
#   uvicorn   app:app --workers 4
#   hypercorn app:app --workers 4
#   granian   --interface asgi app:app --workers 4
app = asgi()

# `tina4 serve` runs this file directly and takes this path.
if __name__ == "__main__":
    run()
