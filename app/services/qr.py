import base64
import io

import qrcode
import qrcode.constants

from app.constants import UPI_CURRENCY, UPI_SCHEME


def build_upi_uri(
    vpa: str,
    payee_name: str,
    *,
    am: str | None = None,
    tn: str | None = None,
) -> str:
    """Build a ``upi://pay`` deep link URI with the given P2P parameters."""
    uri = f"{UPI_SCHEME}?pa={vpa}&pn={payee_name}&cu={UPI_CURRENCY}"
    if am is not None:
        uri += f"&am={am}"
    if tn is not None:
        uri += f"&tn={tn}"
    return uri


def generate_qr_png(data: str) -> bytes:
    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_H)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr_data_uri(data: str) -> str:
    """Generate a base64 data URI from a QR PNG, for embedding in HTML."""
    b64 = base64.b64encode(generate_qr_png(data)).decode("ascii")
    return f"data:image/png;base64,{b64}"
