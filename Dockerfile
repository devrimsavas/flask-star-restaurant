FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

WORKDIR /app

# Install dependencies first so this layer is cached between code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user and give it a writable data folder
RUN useradd --create-home appuser \
    && mkdir -p /data \
    && chown appuser /data
USER appuser

EXPOSE 3000

# Single worker: the menu lives in memory and orders are stored in a JSON file
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "1", "--threads", "4", "app:app"]