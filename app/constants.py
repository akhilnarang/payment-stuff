from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "banks.json"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

UPI_SCHEME = "upi://pay"
UPI_CURRENCY = "INR"

APP_TITLE = "Payment Stuff"
