from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app import models, schemas


# === Functions for Categories ===

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(models.Category).filter(models.Category.id == category_id))
    return result.scalars().first()


async def get_category_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Category).filter(models.Category.name == name))
    return result.scalars().first()


async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(db: AsyncSession, category_id: int, category: schemas.CategoryUpdate):
    await db.execute(update(models.Category).where(models.Category.id == category_id).values(name=category.name))
    await db.commit()


async def delete_category(db: AsyncSession, category_id: int):
    await db.execute(delete(models.Category).where(models.Category.id == category_id))
    await db.commit()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Category).offset(skip).limit(limit))
    return result.scalars().all()


# === Functions for Products ===

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).filter(models.Product.id == product_id))
    return result.scalars().first()


async def get_product_by_name(db: AsyncSession, product_name: str):
    result = await db.execute(select(models.Product).filter(models.Product.name == product_name))
    return result.scalars().first()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, category_id=product.category_id, description=product.description,
                                price=product.price)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductUpdate):
    await db.execute(update(models.Product).where(models.Product.id == product_id).values(
        name=product.name,
        category_id=product.category_id,
        price=product.price
    ))
    await db.commit()


async def delete_product(db: AsyncSession, product_id: int):
    await db.execute(delete(models.Product).where(models.Product.id == product_id))
    await db.commit()


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()


# === Functions for Orders ===

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    return result.scalars().first()


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    product = await db.execute(select(models.Product).filter(models.Product.id == order.product_id))
    product_price = product.scalars().first().price
    total_price = product_price * order.quantity

    db_order = models.Order(customer_id=order.customer_id, product_id=order.product_id, quantity=order.quantity, total_price=total_price)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderUpdate):
    product = await db.execute(select(models.Product).filter(models.Product.id == order.product_id))
    product_price = product.scalars().first().price
    total_price = product_price * order.quantity

    await db.execute(update(models.Order).where(models.Order.id == order_id).values(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price
    ))
    await db.commit()


async def delete_order(db: AsyncSession, order_id: int):
    await db.execute(delete(models.Order).where(models.Order.id == order_id))
    await db.commit()


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()


# === Functions for Customers ===

async def get_customer(db: AsyncSession, customer_id: int):
    result = await db.execute(select(models.Customer).filter(models.Customer.id == customer_id))
    return result.scalars().first()


async def get_customer_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.Customer).filter(models.Customer.username == username))
    return result.scalars().first()


async def create_customer(db: AsyncSession, customer: schemas.CustomerCreate):
    db_customer = models.Customer(username=customer.username, password=customer.password)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


async def update_customer(db: AsyncSession, customer_id: int, customer: schemas.CustomerUpdate):
    await db.execute(update(models.Customer).where(models.Customer.id == customer_id).values(
        username=customer.username,
        password=customer.password
    ))
    await db.commit()


async def delete_customer(db: AsyncSession, customer_id: int):
    await db.execute(delete(models.Customer).where(models.Customer.id == customer_id))
    await db.commit()


async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Customer).offset(skip).limit(limit))
    return result.scalars().all()
