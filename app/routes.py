from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import HTMLResponse

from app.qr import build_upi_uri, generate_qr_png

if TYPE_CHECKING:
    from app.data import Banks

router = APIRouter()
_banks: dict[str, object] = {}


def init_banks(banks: Banks) -> None:
    _banks.update(banks)


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    items = "".join(
        f'<li><a href="/{slug}">{info["bank_name"]}</a></li>'  # type: ignore[index]
        for slug, info in _banks.items()
    )
    return f"<h1>Payment Links</h1><ul>{items}</ul>"


@router.get("/{bank_slug}", response_class=HTMLResponse)
def bank_page(bank_slug: str) -> str:
    info = _banks.get(bank_slug)
    if info is None:
        raise HTTPException(status_code=404, detail="Bank not found")

    bank_name = info["bank_name"]  # type: ignore[index]
    vpa = info["vpa"]  # type: ignore[index]

    html = f"<h1>{bank_name}</h1>"
    html += f"<p>VPA: <code>{vpa}</code></p>"

    if ifsc := info.get("ifsc"):  # type: ignore[union-attr]
        html += f"<p>IFSC: <code>{ifsc}</code></p>"
    if account_number := info.get("account_number"):  # type: ignore[union-attr]
        html += f"<p>Account Number: <code>{account_number}</code></p>"

    html += f'<p><a href="/{bank_slug}/qr">View QR Code</a></p>'
    return html


@router.get("/{bank_slug}/qr")
def bank_qr(
    bank_slug: str,
    am: Annotated[str | None, Query(description="Payment amount")] = None,
    tn: Annotated[str | None, Query(description="Transaction note")] = None,
) -> Response:
    info = _banks.get(bank_slug)
    if info is None:
        raise HTTPException(status_code=404, detail="Bank not found")

    uri = build_upi_uri(
        vpa=info["vpa"],  # type: ignore[index]
        payee_name=info["bank_name"],  # type: ignore[index]
        am=am,
        tn=tn,
    )
    png = generate_qr_png(uri)
    return Response(content=png, media_type="image/png")
