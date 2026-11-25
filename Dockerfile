FROM python:3.13-slim-trixie

LABEL org.opencontainers.image.source=https://github.com/raackley/vaultwarden-backup
LABEL org.opencontainers.image.description="Backup Vaultwarden to AWS S3 and/or Oracle Cloud Object Storage"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN useradd --create-home appuser
USER appuser

CMD ["python", "vaultwarden-backup.py"]