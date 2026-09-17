import base64
import io
import re
import secrets
from urllib.parse import quote, urlencode

import qrcode
import qrcode.constants

from app.constants import UPI_CURRENCY, UPI_SCHEME

_AMOUNT_RE = re.compile(r"^\d+(\.\d{1,2})?$")
# Whole rupees at the low end; the usual UPI per-transaction cap at the top,
# above which the bank would decline anyway. Bounding here also keeps every
# accepted amount inside JS's exact integer range.
MIN_PAISE = 1_00
MAX_PAISE = 100_000_00


def normalize_amount(raw: str) -> str:
    """Normalise an amount to the ``123.45`` form UPI expects.

    Rejects more than two decimal places, scientific notation, negatives and
    anything outside MIN_PAISE..MAX_PAISE rather than silently rounding money.
    """
    raw = raw.strip()
    if not _AMOUNT_RE.match(raw):
        msg = f"amount must be a number with up to two decimal places, got {raw!r}"
        raise ValueError(msg)
    whole, _, frac = raw.partition(".")
    paise = int(whole) * 100 + int(frac.ljust(2, "0"))
    if not MIN_PAISE <= paise <= MAX_PAISE:
        msg = f"amount must be between {MIN_PAISE // 100} and {MAX_PAISE // 100}"
        raise ValueError(msg)
    return f"{paise // 100}.{paise % 100:02d}"


def build_upi_uri(
    vpa: str,
    payee_name: str,
    *,
    am: str | None = None,
    tn: str | None = None,
) -> str:
    """Build a ``upi://pay`` deep link URI with the given P2P parameters.

    ``am`` must already be normalised -- callers take untrusted input, so they
    own the validation and the error response.
    """
    # tr: NPCI transaction reference, max 35 chars. Fresh per URI.
    params = {"pa": vpa, "pn": payee_name, "cu": UPI_CURRENCY, "tr": secrets.token_hex(10)}
    if am is not None:
        params["am"] = am
    if tn is not None:
        params["tn"] = tn
    # quote_via=quote so spaces encode as %20: NPCI's spec percent-encodes the
    # space, and "+" is form encoding that not every app decodes back to one.
    return f"{UPI_SCHEME}?{urlencode(params, quote_via=quote)}"


def generate_qr_png(data: str) -> bytes:
    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_H)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr_data_uri(data: str) -> str:
    """Generate a base64 data URI from a QR PNG, for embedding in HTML."""
    b64 = base64.b64encode(generate_qr_png(data)).decode("ascii")
    return f"data:image/png;base64,{b64}"
