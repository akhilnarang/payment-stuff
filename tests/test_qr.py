import pytest

from app.services.qr import (
    build_upi_uri,
    generate_qr_data_uri,
    generate_qr_png,
    new_tr,
    normalize_amount,
)


def test_basic_uri() -> None:
    uri = build_upi_uri("test@upi", "Test Bank", tr="abc123")
    assert uri == "upi://pay?pa=test%40upi&pn=Test%20Bank&cu=INR&tr=abc123"


def test_uri_with_amount() -> None:
    uri = build_upi_uri("test@upi", "Test Bank", am="100.00")
    assert "&am=100.00" in uri


def test_uri_with_all_params() -> None:
    uri = build_upi_uri("test@upi", "Test Bank", am="50", tn="Lunch", tr="ref1")
    assert uri == "upi://pay?pa=test%40upi&pn=Test%20Bank&cu=INR&tr=ref1&am=50.00&tn=Lunch"


def test_uri_always_carries_a_transaction_reference() -> None:
    assert "&tr=" in build_upi_uri("test@upi", "Test Bank")
    assert new_tr() != new_tr()


def test_uri_escapes_separators_in_note() -> None:
    """A raw & or = in the note must not forge extra UPI parameters."""
    uri = build_upi_uri("test@upi", "Test Bank", am="1", tn="chai & samosa&am=9999")
    assert uri.count("&am=") == 1
    assert "&am=1.00" in uri
    assert "chai%20%26%20samosa%26am%3D9999" in uri


def test_uri_encodes_spaces_as_percent20_not_plus() -> None:
    """UPI apps render a literal "+" in the payee name instead of a space."""
    assert "+" not in build_upi_uri("test@upi", "Some Long Bank Name")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("100", "100.00"),
        ("100.0", "100.00"),  # what str(path_am: float) produces for /bank/100
        ("100.5", "100.50"),
        ("100.50", "100.50"),
        (" 1 ", "1.00"),
        ("1.5", "1.50"),
        ("007", "7.00"),
        ("100000", "100000.00"),  # the cap itself
    ],
)
def test_normalize_amount(raw: str, expected: str) -> None:
    assert normalize_amount(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "12.345",
        "0.99",  # under the floor
        "1e+16",
        "-5",
        "0",
        "0.00",
        "abc",
        "",
        "100,00",
        "1.2.3",
        "100000.01",  # a paisa over the cap
        "1" + "0" * 309 + ".01",  # the magnitude that broke the number input
    ],
)
def test_normalize_amount_rejects(raw: str) -> None:
    with pytest.raises(ValueError, match="amount"):
        normalize_amount(raw)


def test_generate_qr_png_returns_png_bytes() -> None:
    data = generate_qr_png("upi://pay?pa=test@upi&pn=Test")
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_generate_qr_data_uri() -> None:
    uri = generate_qr_data_uri("upi://pay?pa=test@upi&pn=Test")
    assert uri.startswith("data:image/png;base64,")
