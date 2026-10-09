FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    MAIL_RELAY_HOST=relay \
    MAIL_RELAY_PORT=2525

WORKDIR /app
COPY repo/ /app/
COPY sink/ /opt/sink/
