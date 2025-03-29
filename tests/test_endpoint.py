import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_session
from app.main import app

# Создаем отдельный асинхронный двигатель и сессию для тестов
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/wallet_test_db"


@pytest_asyncio.fixture(scope="module")
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Создаем базу данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Мокируем зависимость в FastAPI для использования тестовой сессии
    async def override_get_db():
        async with async_session() as db:
            yield db

    app.dependency_overrides[get_session] = override_get_db

    yield async_session()  # Возвращаем асинхронную сессию

    # Удаляем таблицы после тестирования
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_client(test_db):
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.mark.asyncio
async def test_create_wallet(test_client):
    response = await test_client.post("/wallets-create/", json={"address": "TXYZ12345"})
    assert response.status_code == 200
    assert response.json()["address"] == "TXYZ12345"


@pytest.mark.asyncio
async def test_read_wallets(test_client):
    response = await test_client.get("/wallets-info/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.asyncio
async def test_read_wallets_count(test_client):
    await test_create_wallet(test_client)
    await test_create_wallet(test_client)
    await test_create_wallet(test_client)
    response = await test_client.get("/wallets-info/?skip=0&limit=2")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
