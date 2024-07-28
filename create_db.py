from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Настройки подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/name_db"

# Создаем объект engine
engine = create_engine(DATABASE_URL)

# Создаем базовый класс
Base = declarative_base()

# Определение моделей
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    orders = relationship('Order', back_populates='customer')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')
    orders = relationship('Order', back_populates='product')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    customer = relationship('Customer', back_populates='orders')
    product = relationship('Product', back_populates='orders')


# Код для создания таблиц
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
