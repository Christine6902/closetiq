"""Auth helpers — session guard and context injection."""


def require_login(request, response):
    """Check if the user is logged in. Returns (user_id, None) or (None, redirect)."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None, response.redirect("/login")
    return user_id, None


def auth_context(request):
    """Return template context dict with session user info."""
    return {
        "session_user_name": request.session.get("user_name") or "",
        "session_user_id": request.session.get("user_id"),
    }
