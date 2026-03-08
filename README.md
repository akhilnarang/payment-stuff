# payment-stuff

UPI payment link and QR code generator.

## Docker

```sh
docker run -d \
  -p 8000:8000 \
  -v /path/to/banks.json:/app/data/banks.json:ro \
  ghcr.io/<owner>/payment-stuff
```

`banks.json` format:

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

### Routes

| Route | Description |
|---|---|
| `/` | List all banks |
| `/{slug}` | Bank details (VPA, IFSC, account number) |
| `/{slug}/qr` | UPI QR code (PNG) |

QR query params: `am` (amount), `tn` (transaction note).
