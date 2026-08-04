FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libssl-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

RUN groupadd -r appgroup && \
    useradd -r -g appgroup -m appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium and its Linux dependencies in the shared location.
RUN python -m playwright install --with-deps chromium

COPY . .

RUN chown -R appuser:appgroup /app /ms-playwright

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]