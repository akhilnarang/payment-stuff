import json
from pathlib import Path

from pydantic import BaseModel

from app.constants import DATA_PATH


class BankInfo(BaseModel):
    bank_name: str
    vpa: str
    ifsc: str | None = None
    account_number: str | None = None


type Banks = dict[str, BankInfo]

banks: Banks = {}


def load_banks(path: Path = DATA_PATH) -> None:
    """Load bank data from JSON into the module-level ``banks`` dict."""
    with path.open() as f:
        raw: dict[str, dict[str, str]] = json.load(f)
    banks.update({slug: BankInfo(**data) for slug, data in raw.items()})
