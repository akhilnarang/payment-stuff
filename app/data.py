import json
from pathlib import Path
from typing import TypedDict

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "banks.json"


class BankInfo(TypedDict, total=False):
    bank_name: str
    vpa: str
    ifsc: str
    account_number: str


type Banks = dict[str, BankInfo]


def load_banks(path: Path = DATA_PATH) -> Banks:
    with path.open() as f:
        return json.load(f)
