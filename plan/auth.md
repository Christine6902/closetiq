# Feature: Authentication & User Isolation

**Outcome:** Every wardrobe is private. Unauthenticated visitors see only the login page. Create/delete endpoints require a logged-in session. Each user sees only their own items.

## Scope
- [ ] Migration 000002: `user` table + `user_id` column on `wardrobe_item` (default 1 for seed data)
- [ ] User ORM model (email, password_hash, display_name)
- [ ] POST /api/register (@noauth) — create account, start session
- [ ] POST /api/login (@noauth) — verify password, start session
- [ ] GET /logout — clear session, redirect to login
- [ ] GET /login — login/register page (Frond template)
- [ ] Session middleware — redirect unauthenticated users to /login
- [ ] Scope wardrobe queries to session user_id
- [ ] Scope outfit generation to session user_id
- [ ] Scope dashboard stats to session user_id
- [ ] Remove @noauth from create/delete wardrobe routes
- [ ] Nav: show user name + logout link when logged in
- [ ] Persistent uploads volume in Dockerfile

## Tests
- [ ] register creates user, starts session
- [ ] login with correct password starts session
- [ ] login with wrong password returns 401
- [ ] unauthenticated request redirects to /login
- [ ] user A cannot see user B's items
- [ ] delete only works on own items

## Bugs
(none yet)

## Commits
(pending)

## Status: In Progress
