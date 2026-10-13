"""User manual route — in-app how-to guide."""
from tina4_python.core.router import get
from tina4_python.swagger import description, tags
from src.app.auth_helpers import require_login, auth_context


@description("Render the how-to user manual page.")
@tags(["pages"])
@get("/manual")
async def manual_page(request, response):
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    return response.render("manual.twig", {
        **auth_context(request),
        "nav_active": "manual",
        "title": "How To Use ClosetIQ",
    })
