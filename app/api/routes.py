from typing import Annotated

from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.constants import TEMPLATES_DIR
from app.data import banks
from app.services.helpers import get_bank_or_404
from app.services.qr import build_upi_uri, generate_qr_data_uri

router = APIRouter()
_templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> Response:
    return _templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"banks": banks},
    )


@router.get("/{bank_slug}", response_class=HTMLResponse)
def bank_page(request: Request, bank_slug: str) -> Response:
    info = get_bank_or_404(bank_slug)
    return _templates.TemplateResponse(
        request=request,
        name="bank.html",
        context={"info": info, "slug": bank_slug},
    )


@router.get("/{bank_slug}/qr", response_class=HTMLResponse)
@router.get("/{bank_slug}/{path_am:float}", response_class=HTMLResponse)
def bank_qr(
    request: Request,
    bank_slug: str,
    path_am: float | None = None,
    am: Annotated[str | None, Query(description="Payment amount")] = None,
    tn: Annotated[str | None, Query(description="Transaction note")] = None,
) -> Response:
    info = get_bank_or_404(bank_slug)
    if path_am is not None:
        am = str(path_am)

    uri = build_upi_uri(
        vpa=info.vpa,
        payee_name=info.bank_name,
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
            "upi_uri": uri,
            "qr_data_uri": generate_qr_data_uri(uri),
        },
    )
