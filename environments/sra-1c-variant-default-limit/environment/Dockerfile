FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    SYNC_API_URL=http://api:9000 \
    SYNC_API_KEY=atlas_dev_key_1

WORKDIR /app
COPY repo/ /app/
COPY mock/ /opt/mock/
