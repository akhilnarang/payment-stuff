from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.qr import build_upi_uri, generate_qr_data_uri

if TYPE_CHECKING:
    from app.data import Banks

router = APIRouter()
_banks: dict[str, object] = {}
_templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


def init_banks(banks: Banks) -> None:
    _banks.update(banks)


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> Response:
    return _templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"banks": _banks},
    )


@router.get("/{bank_slug}", response_class=HTMLResponse)
def bank_page(request: Request, bank_slug: str) -> Response:
    info = _banks.get(bank_slug)
    if info is None:
        raise HTTPException(status_code=404, detail="Bank not found")

    return _templates.TemplateResponse(
        request=request,
        name="bank.html",
        context={"info": info, "slug": bank_slug},
    )


@router.get("/{bank_slug}/qr", response_class=HTMLResponse)
@router.get("/{bank_slug}/{path_am:int}", response_class=HTMLResponse)
def bank_qr(
    request: Request,
    bank_slug: str,
    path_am: int | None = None,
    am: Annotated[str | None, Query(description="Payment amount")] = None,
    tn: Annotated[str | None, Query(description="Transaction note")] = None,
) -> Response:
    info = _banks.get(bank_slug)
    if info is None:
        raise HTTPException(status_code=404, detail="Bank not found")

    if path_am is not None:
        am = str(path_am)

    uri = build_upi_uri(
        vpa=info["vpa"],  # type: ignore[index]
        payee_name=info["bank_name"],  # type: ignore[index]
        am=am,
        tn=tn,
    )
    return _templates.TemplateResponse(
        request=request,
        name="qr.html",
        context={
            "info": info,
            "slug": bank_slug,
            "am": am,
            "tn": tn,
            "qr_data_uri": generate_qr_data_uri(uri),
        },
    )
