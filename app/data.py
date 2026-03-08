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

banks: Banks = {}


def load_banks(path: Path = DATA_PATH) -> None:
    with path.open() as f:
        banks.update(json.load(f))
