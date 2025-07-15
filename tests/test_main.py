# tests/test_main.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models, database 

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    app.dependency_overrides[database.get_db] = override_get_db

@pytest.mark.asyncio
async def test_root_redirect():
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.url.path == "/docs"

@pytest.mark.asyncio
async def test_shorten_url():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/")

@pytest.mark.asyncio
async def test_redirect_url():
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=False) as ac:
        # First, create a shortened URL
        post_response = await ac.post("/shorten", json={"original_url": "https://example.com"})
        assert post_response.status_code == 200
        short_url = post_response.json()["short_url"]
        short_code = short_url.rsplit("/", 1)[-1]

        # Then, test redirect
        get_response = await ac.get(f"/{short_code}")
        assert get_response.status_code in (302, 307)
        assert get_response.headers["location"] == "https://example.com"
