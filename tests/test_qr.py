from app.qr import build_upi_uri, generate_qr_data_uri, generate_qr_png


def test_basic_uri() -> None:
    uri = build_upi_uri("test@upi", "Test Bank")
    assert uri == "upi://pay?pa=test@upi&pn=Test Bank&cu=INR"


def test_uri_with_amount() -> None:
    uri = build_upi_uri("test@upi", "Test Bank", am="100.00")
    assert "&am=100.00" in uri


def test_uri_with_all_params() -> None:
    uri = build_upi_uri(
        "test@upi",
        "Test Bank",
        am="50",
        tn="Lunch",
    )
    assert "&am=50" in uri
    assert "&tn=Lunch" in uri


def test_generate_qr_png_returns_png_bytes() -> None:
    data = generate_qr_png("upi://pay?pa=test@upi&pn=Test")
    assert data[:8] == b"\x89PNG\r\n\x1a\n"


def test_generate_qr_data_uri() -> None:
    uri = generate_qr_data_uri("upi://pay?pa=test@upi&pn=Test")
    assert uri.startswith("data:image/png;base64,")
