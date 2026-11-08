# KisanSamvaad - Sovereign Indic Agricultural AI Server
# Lightweight Multi-Platform Docker Container (<100MB RAM Target)

FROM python:3.11-slim AS runtime

# Set environment flags for predictable standard library execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    HOST=0.0.0.0 \
    PORT=8000

# Install curl for container health check
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user
RUN groupadd -r kisan && useradd -r -g kisan -d /app kisan

WORKDIR /app

# Copy application backend, frontend, and documentation
COPY --chown=kisan:kisan backend/ /app/backend/
COPY --chown=kisan:kisan frontend/ /app/frontend/
COPY --chown=kisan:kisan docs/ /app/docs/

# Create persistent storage directory for SQLite database
RUN mkdir -p /app/data && chown -R kisan:kisan /app/data

# Switch to non-root user
USER kisan

# Expose HTTP port
EXPOSE 8000

# Container Healthcheck (every 30s, 5s timeout, 3 retries)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/api/health || exit 1

# Launch server
CMD ["python", "backend/server.py", "8000"]

