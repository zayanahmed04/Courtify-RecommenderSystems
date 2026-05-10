FROM python:3.11-slim AS base

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Dependency layer (cached unless requirements.txt changes) ---
FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Application layer ---
FROM deps AS app

COPY . .

# Create directories that will be populated at runtime or via volume
RUN mkdir -p data/models data/processed data/raw

# Non-root user for security
RUN useradd -m -u 1001 courtfind && chown -R courtfind:courtfind /app
USER courtfind

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "2", "--log-level", "info"]
