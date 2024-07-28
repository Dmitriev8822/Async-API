# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.database import SessionLocal, engine

from fastapi import Depends, HTTPException, status

app = FastAPI()


# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session


# --- Обработка маршрутов сущности "categories" ---

# Асинхронная функция 'create_category' используется для создания новой категории
@app.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли категория с таким же именем
    db_category = await crud.get_category_by_name(db, name=category.name)
    if db_category:
        # Если категория уже существует, возвращаем ошибку с кодом 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Category already registered")

    # Создаем новую категорию
    return await crud.create_category(db, category)


# Асинхронная функция 'read_category' используется для чтения информации о категории по ID
@app.get("/categories/{category_id}", response_model=schemas.Category)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    # Получение категории из базы данных по ID
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        # Если категория не найдена, вызываем исключение HTTP 404 (Not Found)
        raise HTTPException(status_code=404, detail="Category not found")

    # Возвращаем информацию о категории
    return db_category


# Асинхронная функция 'update_category' используется для обновления информации о категории по ID
@app.put("/categories/{category_id}", response_model=schemas.Category)
async def update_category(category_id: int, category: schemas.CategoryUpdate, db: AsyncSession = Depends(get_db)):
    # Проверка на наличие другой категории с таким же именем в базе данных
    db_category = await crud.get_category_by_name(db, name=category.name)
    if db_category:
        # Если категория с таким именем уже существует, вызываем исключение 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Category already registered")

    # Обновление категории с помощью crud функции
    await crud.update_category(db, category_id, category)

    # Получаем обновленную категорию из базы данных
    return await crud.get_category(db, category_id)


# Асинхронная функция 'delete_category' используется для удаления информации о категории по ID
@app.delete("/categories/{category_id}", response_model=schemas.Category)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    # Попытка получения категории из базы данных по её ID
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        # Если категория не найдена, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Category not found")

    # Удаление категории через crud функцию
    await crud.delete_category(db, category_id)

    # Возвращаем информацию об удалённой категории
    return db_category


# Асинхронная функция 'read_categories' используется для чтения информации о всех категориях в базе данных
@app.get("/categories/", response_model=list[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Получение списка категорий из базы данных с применением параметров пагинации
    return await crud.get_categories(db, skip=skip, limit=limit)


# --- Обработка маршрутов сущности "products" ---

# Асинхронная функция 'create_product' используется для создания нового продукта
@app.post("/products/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли продукт с таким же именем
    db_product = await crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        # Если продукт уже существует, возвращаем ошибку с кодом 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Product already registered")

    db_category = await crud.get_category(db, category_id=product.category_id)
    if db_category is None:
        # Если продукт не найден, возвращаем ошибку с кодом 404 (Not Found)
        raise HTTPException(status_code=404, detail="Category not found")

    # Создаем новый продукт
    return await crud.create_product(db, product)


# Асинхронная функция 'read_product' используется для чтения информации о продукте по ID
@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # Получение продукта из базы данных по ID
    db_product = await crud.get_product(db, product_id)
    if db_product is None:
        # Если категория не найдена, вызываем исключение HTTP 404 (Not Found)
        raise HTTPException(status_code=404, detail="Product not found")

    # Возвращаем информацию о категории
    return db_product


# Асинхронная функция 'update_product' используется для обновления информации о продукте по ID
@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    # Проверка на наличие другого продукта с таким же именем в базе данных
    db_product = await crud.get_product_by_name(db, product_name=product.name)
    if db_product and db_product.id != product_id:
        # Если категория с таким именем уже существует, вызываем исключение HTTP 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Product already registered")

    # Получаем продукт из базы данных по ID
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        # Если продукт не найден, возвращаем ошибку с кодом 404 (Not Found)
        raise HTTPException(status_code=404, detail="Customer not found")

    # Обновление продукта с помощью crud функций
    await crud.update_product(db, product_id, product)
    # Возвращаем обновленный продукт
    return await crud.get_product(db, product_id)


# Асинхронная функция 'delete_product' используется для удаления информации о продукте по ID
@app.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем продукт из базы данных по ID
    db_product = await crud.get_product(db, product_id)
    if db_product is None:
        # Если продукт не найден, возвращаем ошибку с кодом 404 (Not Found)
        raise HTTPException(status_code=404, detail="Product not found")

    # Удаление продукта через crud функцию
    await crud.delete_product(db, product_id)
    # Возвращаем информацию о продукте
    return db_product


# Асинхронная функция 'read_products' используется для чтения информации о всех продуктах в базе данных
@app.get("/products/", response_model=list[schemas.Product])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Получение списка продуктов из базы данных с применением параметров пагинации
    return await crud.get_products(db, skip=skip, limit=limit)


# --- Обработка маршрутов сущности "order" ---

# Асинхронная функция 'create_order' используется для создания нового заказа
@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем по ID, существует ли пользователь
    db_customer = await crud.get_customer(db, order.customer_id)
    # Проверяем по ID, существует ли продукт
    db_product = await crud.get_product(db, order.product_id)
    if (db_customer is None) or (db_product is None):
        # Если продукт или пользователь не найден, возвращаем ошибку с кодом 404 (Not Found)
        error = "Customer not found" if db_customer is None else "Product not found"
        raise HTTPException(status_code=404, detail=error)

    # Создаем новый заказ
    return await crud.create_order(db, order)


# Асинхронная функция 'read_order' используется для чтения информации о заказе по ID
@app.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    # Получение заказа из базы данных по ID
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        # Если заказ не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Order not found")

    # Возвращаем информацию о категории
    return db_order


# Асинхронная функция 'update_order' используется для обновления информации о заказе по ID
@app.put("/orders/{order_id}", response_model=schemas.Order)
async def update_order(order_id: int, order: schemas.OrderUpdate, db: AsyncSession = Depends(get_db)):
    # Проверяем по ID, существует ли пользователь
    db_customer = await crud.get_customer(db, order.customer_id)
    # Проверяем по ID, существует ли продукт
    db_product = await crud.get_product(db, order.product_id)
    if (db_customer is None) or (db_product is None):
        # Если продукт или пользователь не найден, возвращаем ошибку с кодом 404 (Not Found)
        error = "Customer not found" if db_customer is None else "Product not found"
        raise HTTPException(status_code=404, detail=error)

    # Получение заказа из базы данных по ID
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        # Если заказ не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Order not found")

    # Обновление заказа с помощью crud функций
    await crud.update_order(db, order_id, order)
    # Возвращаем обновленный заказ
    return await crud.get_order(db, order_id)


# Асинхронная функция 'delete_order' используется для удаления информации о заказе по ID
@app.delete("/orders/{order_id}", response_model=schemas.Order)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    # Получение заказа из базы данных по ID
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        # Если заказ не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Order not found")

    # Удаление заказа c помощью crud функций
    await crud.delete_order(db, order_id)
    # Возвращаем удаленный заказ
    return db_order


# Асинхронная функция 'read_orders' используется для чтения информации о всех заказах в базе данных
@app.get("/orders/", response_model=list[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Получение списка заказов из базы данных с применением параметров пагинации
    return await crud.get_orders(db, skip=skip, limit=limit)


# --- Обработка маршрутов сущности "customers" ---

# Асинхронная функция 'create_customer' используется для создания нового пользователя
@app.post("/customers/", response_model=schemas.Customer)
async def create_customer(customer: schemas.CustomerCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким же именем
    db_customer = await crud.get_customer_by_username(db, username=customer.username)
    if db_customer:
        # Если пользователь уже существует, возвращаем ошибку с кодом 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Username already registered")

    # Создаем нового пользователя
    return await crud.create_customer(db, customer)


# Асинхронная функция 'read_customer' используется для чтения информации о пользователе по ID
@app.get("/customers/{customer_id}", response_model=schemas.Customer)
async def read_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    # Получение пользователя из базы данных по ID
    db_customer = await crud.get_customer(db, customer_id)
    if db_customer is None:
        # Если пользователь не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Customer not found")

    # Возвращаем информацию о пользователе
    return db_customer


# Асинхронная функция 'update_customer' используется для обновления информации о пользователе по ID
@app.put("/customers/{customer_id}", response_model=schemas.Customer)
async def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким же именем
    db_customer = await crud.get_customer_by_username(db, username=customer.username)
    if db_customer and db_customer.id != customer_id:
        # Если пользователь уже существует, возвращаем ошибку с кодом 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Username already registered")

    # Получение пользователя из базы данных по ID
    db_customer = await crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        # Если пользователь не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Customer not found")

    # Обновление пользователя с помощью crud функции
    await crud.update_customer(db, customer_id, customer)
    # Возвращаем данные пользователя
    return await crud.get_customer(db, customer_id)


# Асинхронная функция 'delete_customer' используется для удаления пользователя по ID
@app.delete("/customers/{customer_id}", response_model=schemas.Customer)
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    # Получение пользователя из базы данных по ID
    db_customer = await crud.get_customer(db, customer_id)
    if db_customer is None:
        # Если пользователь не найден, вызываем исключение 404 (Not Found)
        raise HTTPException(status_code=404, detail="Customer not found")

    # Удаление пользователя с помощью crud функции
    await crud.delete_customer(db, customer_id)
    # Возвращаем данные удалённого пользователя
    return db_customer


# Асинхронная функция 'read_customers' используется для чтения списка пользователей
@app.get("/customers/", response_model=list[schemas.Customer])
async def read_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Получение списка пользователей из базы данных
    return await crud.get_customers(db, skip=skip, limit=limit)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000)
    pass
