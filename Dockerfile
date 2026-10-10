# ClosetIQ — production container
FROM python:3.14-slim AS base

# System deps for SQLite (included in slim) and healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (cached layer)
COPY pyproject.toml ./
RUN pip install --no-cache-dir . uvicorn[standard]

# Copy application code
COPY app.py ./
COPY src/ src/
COPY migrations/ migrations/
COPY design/ design/

# Ensure data directory exists for SQLite
RUN mkdir -p data

# Production environment
ENV TINA4_DEBUG=false
ENV TINA4_LOG_LEVEL=INFO
ENV TINA4_DATABASE_URL=sqlite:///data/app.db
ENV TINA4_NO_BROWSER=true
ENV PORT=8000

EXPOSE 8000

# Run migrations then start the ASGI server
CMD sh -c "python -m tina4_python migrate 2>/dev/null; \
    uvicorn app:app --host 0.0.0.0 --port ${PORT} --workers 2 --log-level info"
