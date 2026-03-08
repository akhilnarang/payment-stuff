import base64
import io

import qrcode
import qrcode.constants


def build_upi_uri(
    vpa: str,
    payee_name: str,
    *,
    am: str | None = None,
    tn: str | None = None,
) -> str:
    uri = f"upi://pay?pa={vpa}&pn={payee_name}&cu=INR"
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
    png = generate_qr_png(data)
    b64 = base64.b64encode(png).decode("ascii")
    return f"data:image/png;base64,{b64}"
