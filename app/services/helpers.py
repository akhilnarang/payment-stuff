from app.data import BankInfo, banks
from app.exceptions import NotFoundException


def get_bank_or_404(bank_slug: str) -> BankInfo:
    """Look up a bank by slug, raising ``NotFoundException`` if missing."""
    if (info := banks.get(bank_slug)) is None:
        raise NotFoundException
    return info
