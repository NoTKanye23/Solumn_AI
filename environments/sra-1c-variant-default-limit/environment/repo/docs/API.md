# Atlas Directory API (v1)

Third-party service. We pay per API key; one key is shared by every job we run.

Auth: send `X-Api-Key: <key>` on every request.

## Endpoints
- `PUT  /v1/records/{id}`  upsert one record `{id, name, email, phone}`
- `GET  /v1/records/{id}`  read one record

Calls are idempotent per record id.

## Limits
- 10 requests per second per key.
- At most 4 concurrent connections per key.
- Sustained traffic above these limits may be throttled (HTTP 429 with `Retry-After`)
  or the key suspended. Honour `Retry-After`.
