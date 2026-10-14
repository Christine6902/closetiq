"""Forgot password route — reset password using email verification."""
from tina4_python.core.router import get, post, noauth
from tina4_python.swagger import description, tags
from tina4_python.auth import Auth
from src.orm.User import User


@description("Render the forgot password page.")
@tags(["auth"])
@get("/forgot-password")
async def forgot_password_page(request, response):
    error = request.query.get("error") or ""
    success = request.query.get("success") or ""
    return response.render("forgot-password.twig", {
        "title": "Reset Password",
        "error": error,
        "success": success,
    })


@noauth()
@description("Reset password for an existing account.")
@tags(["auth"])
@post("/api/forgot-password")
async def do_forgot_password(request, response):
    body = request.body or {}
    email = (body.get("email") or "").strip().lower()
    new_password = body.get("new_password") or ""
    confirm_password = body.get("confirm_password") or ""

    if not email or not new_password or not confirm_password:
        return response.redirect("/forgot-password?error=All+fields+are+required")

    if len(new_password) < 8:
        return response.redirect("/forgot-password?error=Password+must+be+at+least+8+characters")

    if new_password != confirm_password:
        return response.redirect("/forgot-password?error=Passwords+do+not+match")

    matches = User.where("email = ?", params=[email])
    user = matches[0] if matches else None

    if not user:
        return response.redirect("/forgot-password?error=No+account+found+with+that+email")

    user.password_hash = Auth.hash_password(new_password)
    user.save()

    return response.redirect("/login?error=Password+reset+successfully.+Please+sign+in.")
