from sqlalchemy.future import select  # Импортируем select
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import WalletInfo


# Настройка временной базы данных для тестов
@pytest_asyncio.fixture
async def test_db():
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/wallet_test_db"
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Создаем базу данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Возвращаем сессию как асинхронный контекст
    async with SessionLocal() as session:
        yield session  # Здесь возвращаем сессию

    # Удаляем все таблицы после тестирования
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Тестирование модели WalletInfo
@pytest.mark.asyncio
async def test_create_wallet_info(test_db):
    wallet = WalletInfo(address="TXYZ", bandwidth=100, energy=50, trx_balance=1000)

    # Начинаем новую транзакцию
    async with test_db.begin():
        test_db.add(wallet)
        await test_db.commit()

    # Проверяем, что данные записаны правильно
    query = select(WalletInfo).filter_by(address="TXYZ")
    result = await test_db.execute(query)
    retrieved_wallet = result.scalars().first()

    assert retrieved_wallet is not None
    assert retrieved_wallet.bandwidth == 100
    assert retrieved_wallet.energy == 50
    assert retrieved_wallet.trx_balance == 1000
