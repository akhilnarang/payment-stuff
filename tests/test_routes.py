from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from app.data import banks, load_banks
from main import app

TEST_DATA = Path(__file__).resolve().parent / "data" / "banks.json"


@pytest.fixture(autouse=True)
def _load_test_data() -> None:
    banks.clear()
    load_banks(TEST_DATA)


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_index(client: AsyncClient) -> None:
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "Test Bank" in resp.text
    assert "Other Bank" in resp.text


@pytest.mark.anyio
async def test_bank_page(client: AsyncClient) -> None:
    resp = await client.get("/testbank")
    assert resp.status_code == 200
    assert "<code>testuser@testbank</code>" in resp.text
    assert "TEST0000001" in resp.text
    assert "1234567890" in resp.text


@pytest.mark.anyio
async def test_bank_page_optional_fields(client: AsyncClient) -> None:
    resp = await client.get("/otherbank")
    assert resp.status_code == 200
    assert "<code>testuser@otherbank</code>" in resp.text


@pytest.mark.anyio
async def test_bank_not_found(client: AsyncClient) -> None:
    resp = await client.get("/nonexistent")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_qr_page(client: AsyncClient) -> None:
    resp = await client.get("/testbank/qr")
    assert resp.status_code == 200
    assert "<code>testuser@testbank</code>" in resp.text
    assert "upi://pay" in resp.text


@pytest.mark.anyio
async def test_qr_with_params(client: AsyncClient) -> None:
    resp = await client.get("/testbank/qr?am=100&tn=test+payment")
    assert resp.status_code == 200
    assert 'value="100"' in resp.text
    assert 'value="test payment"' in resp.text


@pytest.mark.anyio
async def test_qr_short_path(client: AsyncClient) -> None:
    resp = await client.get("/testbank/500")
    assert resp.status_code == 200
    assert 'value="500.0"' in resp.text


@pytest.mark.anyio
async def test_qr_not_found(client: AsyncClient) -> None:
    resp = await client.get("/nonexistent/qr")
    assert resp.status_code == 404
