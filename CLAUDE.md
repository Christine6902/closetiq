# tina4example — Tina4 Python project

You're working in **Claude Desktop**.

**Tina4 v3** — *The Intelligent Native Application 4ramework*. Built for AI:
zero third-party dependencies, convention over configuration, one small
consistent API. Use the framework's built-ins (routing, ORM, migrations, Frond
templates, auth/JWT, queues, cache, sessions, WebSockets, GraphQL) before any
library or hand-rolled code.

## Source of truth — check before you guess

1. **Skills** in `~/.claude/skills/` — **tina4-developer** (+ **tina4-js** for
   the reactive frontend). These document the real API surface.
2. **https://tina4.com** — docs + the **Ask Tina4** RAG box (ask it any
   framework question; it answers from the live corpus).
3. **`/__dev/mcp`** live tools (wired via the `.mcp.json` in this folder) —
   query for real routes, models, and signatures when the dev server is running.

## Environment (.env)

```bash
TINA4_DEBUG=true                              # dev mode: hot-reload, error overlay, /__dev
TINA4_SECRET=change-me                        # JWT signing secret
TINA4_DATABASE_URL=sqlite:///data/app.db      # driver://host:port/db
TINA4_DATABASE_USERNAME=                       # db user (blank for sqlite)
TINA4_DATABASE_PASSWORD=                       # db password
TINA4_LOG_LEVEL=INFO                          # ALL | DEBUG | INFO | WARNING | ERROR
TINA4_API_KEY=                                 # optional static bearer token
TINA4_CACHE_BACKEND=memory                    # memory | file | redis | valkey | memcached | mongodb | database
TINA4_SESSION_BACKEND=file                    # session store
TINA4_NO_BROWSER=false                        # set true to never auto-open the browser
```

## Database & drivers

SQLite works out of the box:

```bash
TINA4_DATABASE_URL=sqlite:///data/app.db   # three slashes = relative to cwd
```

Connection URLs are `driver://host:port/database` (sqlite / postgres / postgresql / mysql / mssql / firebird).

Add a Postgres or MySQL driver:

```bash
uv add psycopg2-binary           # Postgres
uv add mysql-connector-python    # MySQL
```

```bash
TINA4_DATABASE_URL=postgresql://localhost:5432/mydb   # + TINA4_DATABASE_USERNAME / TINA4_DATABASE_PASSWORD
```

## Add a route

`src/routes/hello.py` (auto-discovered; one resource per file):

```python
from tina4_python.core.router import get


@get("/hello")
async def hello(request, response):
    return response({"message": "Hello from Tina4"})
```

## Templates (Frond)

Frond is the built-in zero-dep Twig-compatible engine; templates live in `src/templates/` (`.twig`). Common syntax:

```twig
{% extends "base.twig" %}
{% block content %}
  <h1>{{ title }}</h1>
  <ul>
    {% for x in items %}
      <li>{{ x.name | upper }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

Render it from a route:

```python
return response.render("hello.twig", {"name": "Tina4"})
```

## How to run

```bash
tina4 serve
```

Dev server: watches files, hot-reloads, opens the app + the `/__dev` dashboard.

> Dev runs two ports: the **base** port hot-reloads (for you); **base+1000** is
> stable and does NOT reload — use that one when an AI is driving the browser so
> a reload doesn't interrupt it.

## Where things go

| You want to…            | Put it in…                     | Make it with                                           |
|-------------------------|--------------------------------|--------------------------------------------------------|
| Add a page or API route | `src/routes/`                  | `tina4 generate route <name>`                          |
| Add a database model    | `src/orm/`                     | `tina4 generate model <Name>`                          |
| Change the schema       | `migrations/`                  | `tina4 generate migration <name>` then `tina4 migrate` |
| Add a page template     | `src/templates/`               | Frond (`.twig`)                                        |
| Frontend behaviour      | `tina4-js`                     | tina4-js signals + html templates                      |

## Golden rules

- **Use built-ins first** — Tina4 is zero-dep; reach for the framework before any library or hand-rolled code.
- **Don't guess API names** — check the skills / **Ask Tina4** at https://tina4.com / the live `/__dev/mcp` tools.
- Routes return data; **`response()`** (called, not `response.json`) auto-serializes models, lists, and `DatabaseResult` to JSON.
- **One resource per file** in `src/routes/` and `src/orm/`.
- All schema changes go through migrations (`tina4 generate migration` → `tina4 migrate`) — never raw DDL in routes.
- No inline styles / no hardcoded hex — use tina4-css classes + SCSS in `src/scss/`.
- Env comes from `.env`; `TINA4_DEBUG=true` in dev.
- All links point to **https://tina4.com**.
- **Python gotcha:** route decorators (`@get`/`@post`/…) must be INNERMOST (closest to `def`); `@noauth`/`@secured`/`@description` go above. GET is public; POST/PUT/PATCH/DELETE need auth unless `@noauth()`. Use `response(...)`, not `response.json()`.

## A good first prompt

> Add a `/products` page backed by a `Product` model (name, price, image_url), seed three rows, and render them as cards using a tina4-js component.
