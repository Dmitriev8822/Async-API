# test_main.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Импортируйте ваше приложение FastAPI
from app.database import Base

# Укажите временную базу данных для тестов
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/name_db"

# Создайте временный engine и sessionmaker для тестов
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


# Создайте тестовую сессию и таблицы
@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        # Создаем таблицы
        await conn.run_sync(Base.metadata.create_all)

    # Передаем объект сессии в тесты
    async with SessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        # Удаляем таблицы после тестов
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# Тест создания категории
def test_create_category(client, test_db):
    # Создаём запрос
    response = client.post(
        "/categories/",
        json={"name": "Electronics"}
    )

    # Проверяем корректность ответа
    assert ((response.status_code == 200 and response.json()["name"] == "Electronics") or
            (response.status_code == 400 and response.json()["detail"] == "Category already registered"))


# Тест создания продукта
def test_create_product(client, test_db):
    # Создаём запрос
    response = client.post(
        "/products/",
        json={"name": "Phone",
              "description": "cool phone",
              "price": 10000,
              "category_id": 100}
    )

    # Проверяем корректность ответа
    data = response.json()
    assert ((response.status_code == 200 and data["name"] == "Phone" and data["description"] == "cool phone" and data[
        "price"] == 10000 and data["category_id"] == 8) or
            (response.status_code == 400 and response.json()["detail"] == "Product already registered"))


# Тест создания продукта с несуществующей категорией
def test_create_product_none_category(client, test_db):
    # Создаём запрос
    response = client.post(
        "/products/",
        json={"name": "Unique name",
              "description": "",
              "price": 1,
              "category_id": 100}  # Категория не существует
    )

    # Проверяем корректность ответа
    assert (response.status_code == 404 and response.json()["detail"] == "Category not found")


# Тест создания клиента
def test_create_customer(client, test_db):
    # Создаём запрос
    response = client.post(
        "/customers/",
        json={"username": "User",
              "password": "123"}
    )

    # Проверяем корректность ответа
    data = response.json()
    assert ((response.status_code == 200 and data["username"] == "User" and data["password"] == "123") or (
                response.status_code == 400 and response.json()["detail"] == "Username already registered"))


def test_create_order(client, test_db):
    # Создаём запрос
    response = client.post(
        "/orders/",
        json={"customer_id": 1,
              "product_id": 1,
              "quantity": 1}
    )

    # Проверяем корректность ответа
    data = response.json()
    assert ((response.status_code == 200 and data["customer_id"] == 1 and data["product_id"] == 1 and data["quantity"] == 1) or (
                response.status_code == 404 and (response.json()["detail"] == "Customer not found" or response.json()["detail"] == "Product not found")))


