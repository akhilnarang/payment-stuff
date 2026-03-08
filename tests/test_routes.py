from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.data import load_banks
from app.routes import init_banks
from main import app


@pytest.fixture(autouse=True)
def _load_bank_data() -> None:
    init_banks(load_banks())


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_index(client: AsyncClient) -> None:
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "Slice Small Finance Bank" in resp.text


@pytest.mark.anyio
async def test_bank_page(client: AsyncClient) -> None:
    resp = await client.get("/slice")
    assert resp.status_code == 200
    assert "<code>akhilnarang@slc</code>" in resp.text


@pytest.mark.anyio
async def test_bank_not_found(client: AsyncClient) -> None:
    resp = await client.get("/nonexistent")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_qr_page(client: AsyncClient) -> None:
    resp = await client.get("/slice/qr")
    assert resp.status_code == 200
    assert "data:image/png;base64," in resp.text
    assert "<code>akhilnarang@slc</code>" in resp.text


@pytest.mark.anyio
async def test_qr_with_params(client: AsyncClient) -> None:
    resp = await client.get("/slice/qr?am=100&tn=test+payment")
    assert resp.status_code == 200
    assert "<code>100</code>" in resp.text
    assert "<code>test payment</code>" in resp.text


@pytest.mark.anyio
async def test_qr_short_path(client: AsyncClient) -> None:
    resp = await client.get("/slice/500")
    assert resp.status_code == 200
    assert "data:image/png;base64," in resp.text
    assert "<code>500</code>" in resp.text


@pytest.mark.anyio
async def test_qr_not_found(client: AsyncClient) -> None:
    resp = await client.get("/nonexistent/qr")
    assert resp.status_code == 404
