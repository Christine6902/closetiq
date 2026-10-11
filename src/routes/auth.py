"""Auth routes — register, login, logout (session-based)."""
from datetime import datetime

from tina4_python.core.router import get, post, noauth
from tina4_python.swagger import description, tags
from tina4_python.auth import Auth
from src.orm.User import User


@description("Render the login / register page.")
@tags(["auth"])
@get("/login")
async def login_page(request, response):
    """Show the login form. Redirect to dashboard if already logged in."""
    if request.session.get("user_id"):
        return response.redirect("/")
    error = request.query.get("error") or ""
    tab = request.query.get("tab") or "login"
    return response.render("login.twig", {
        "title": "Sign In",
        "error": error,
        "tab": tab,
    })


@noauth()
@description("Authenticate with email + password. Sets a session and redirects to /.")
@tags(["auth"])
@post("/api/login")
async def do_login(request, response):
    """Verify credentials, start a session, redirect to dashboard."""
    body = request.body or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email or not password:
        return response.redirect("/login?error=Email+and+password+are+required")

    matches = User.where("email = ?", params=[email])
    user = matches[0] if matches else None

    if not user or not Auth.check_password(password, user.password_hash):
        return response.redirect("/login?error=Invalid+email+or+password")

    request.session.set("user_id", user.id)
    request.session.set("user_name", user.display_name)
    return response.redirect("/")


@noauth()
@description("Create a new account. Sets a session and redirects to /.")
@tags(["auth"])
@post("/api/register")
async def do_register(request, response):
    """Create a user, start a session, redirect to dashboard."""
    body = request.body or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    display_name = (body.get("display_name") or "").strip()

    if not email or not password or not display_name:
        return response.redirect("/login?tab=register&error=All+fields+are+required")

    if len(password) < 8:
        return response.redirect("/login?tab=register&error=Password+must+be+at+least+8+characters")

    # Check for existing email
    existing = User.where("email = ?", params=[email])
    if existing:
        return response.redirect("/login?tab=register&error=An+account+with+that+email+already+exists")

    user = User({
        "email": email,
        "password_hash": Auth.hash_password(password),
        "display_name": display_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    user.save()

    request.session.set("user_id", user.id)
    request.session.set("user_name", user.display_name)
    return response.redirect("/")


@description("Log out and redirect to the login page.")
@tags(["auth"])
@get("/logout")
async def logout(request, response):
    """Clear the session and redirect to login."""
    request.session.clear()
    return response.redirect("/login")
