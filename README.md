# payment-stuff

UPI payment link and QR code generator.

## Setup

```sh
uv sync
uv run fastapi dev
```

## Routes

| Route | Description |
|---|---|
| `/` | List all banks |
| `/{slug}` | Bank details (VPA, IFSC, account number) |
| `/{slug}/qr` | QR code page with UPI intent button |
| `/{slug}/{amount}` | QR code page with pre-filled amount |

Query params on `/qr`: `am` (amount), `tn` (transaction note).

## `banks.json`

Create `data/banks.json` (gitignored — contains personal VPAs):

```json
{
  "slug": {
    "bank_name": "Bank Name",
    "vpa": "user@bank",
    "ifsc": "OPTIONAL",
    "account_number": "OPTIONAL"
  }
}
```

## Docker

```sh
docker run -d -p 8000:8000 -v /path/to/banks.json:/app/data/banks.json:ro ghcr.io/akhilnarang/payment-stuff
```

## Checks

```sh
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```
