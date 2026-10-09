# Atlas Directory API (v1)

Third-party service. We pay per API key; one key is shared by every job we run.

Auth: send `X-Api-Key: <key>` on every request.

## Endpoints
- `PUT  /v1/records/{id}`  upsert one record `{id, name, email, phone}`
- `POST /v1/records:bulk`  upsert up to 100 records: `{"records": [{...}, ...]}`
- `GET  /v1/records/{id}`  read one record

All calls are idempotent per record id.

## Limits
- 10 requests per second per key (a bulk call counts as one request).
- At most 4 concurrent connections per key.
- Sustained traffic above these limits may be throttled (HTTP 429 with `Retry-After`)
  or the key suspended. Honour `Retry-After`.
