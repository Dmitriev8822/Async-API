# Async API

## Описание

Этот проект представляет собой асинхронный API для простого интернет-магазина, реализованный с использованием `FastAPI`, `SQLAlchemy`, и `PostgreSQL`. API предоставляет CRUD операции для управления сущностями магазина, такими как покупатели, товары, каталоги и заказы. Проект также включает в себя асинхронные миграции базы данных с использованием `Alembic`.

## Основные функции

1. **Модели базы данных**:
    - Покупатели
    - Товары
    - Каталоги
    - Заказы

2. **CRUD операции**:
    - Получение списка сущностей с пагинацией.
    - Получение конкретной сущности по идентификатору.
    - Создание, редактирование и удаление сущностей с проверкой корректности данных.

3. **Создание заказа**:
    - Ручка API для создания нового заказа и установления всех необходимых связей между заказом, покупателем и товарами.

## Технологии

- **FastAPI**: Веб-фреймворк для создания API на Python.
- **SQLAlchemy**: ORM для работы с базой данных PostgreSQL.
- **Alembic**: Инструмент для управления миграциями базы данных.
- **PostgreSQL**: Реляционная база данных.

## Установка и запуск

1. **Клонируйте репозиторий**:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Создайте виртуальное окружение и установите зависимости**:

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Настройте файл `.env`**:
   
   Создайте файл `.env` в корневом каталоге проекта и добавьте строку подключения к базе данных PostgreSQL:

    ```
    DATABASE_URL=postgresql+asyncpg://user:password@localhost/mydatabase
    ```

4. **Примените миграции базы данных**:

    ```bash
    alembic upgrade head
    ```

5. **Запустите сервер FastAPI**:

    ```bash
    uvicorn main:app --reload
    ```

## API

Документация API доступна по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

## Примеры использования

### Получение списка товаров

```http
GET /products
```

### Создание нового заказа

```http
POST /orders
Content-Type: application/json

{
    "customer_id": 1,
    "product_id": 1,
    "quantity": 2
}
```
