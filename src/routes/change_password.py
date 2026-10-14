"""Change password route — lets logged-in users update their password."""
from tina4_python.core.router import get, post
from tina4_python.swagger import description, tags
from tina4_python.auth import Auth
from src.orm.User import User
from src.app.auth_helpers import require_login, auth_context


@description("Render the change password page.")
@tags(["auth"])
@get("/change-password")
async def change_password_page(request, response):
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    error = request.query.get("error") or ""
    success = request.query.get("success") or ""
    return response.render("change-password.twig", {
        **auth_context(request),
        "nav_active": "change-password",
        "title": "Change Password",
        "error": error,
        "success": success,
    })


@description("Process password change for the logged-in user.")
@tags(["auth"])
@post("/api/change-password")
async def do_change_password(request, response):
    user_id, redirect = require_login(request, response)
    if redirect:
        return redirect

    body = request.body or {}
    current_password = body.get("current_password") or ""
    new_password = body.get("new_password") or ""
    confirm_password = body.get("confirm_password") or ""

    if not current_password or not new_password or not confirm_password:
        return response.redirect("/change-password?error=All+fields+are+required")

    if len(new_password) < 8:
        return response.redirect("/change-password?error=New+password+must+be+at+least+8+characters")

    if new_password != confirm_password:
        return response.redirect("/change-password?error=New+passwords+do+not+match")

    user = User.find(user_id)
    if not user:
        return response.redirect("/login")

    if not Auth.check_password(current_password, user.password_hash):
        return response.redirect("/change-password?error=Current+password+is+incorrect")

    user.password_hash = Auth.hash_password(new_password)
    user.save()

    return response.redirect("/change-password?success=Password+changed+successfully")
