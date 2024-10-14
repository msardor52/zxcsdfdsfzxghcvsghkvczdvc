from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:5052@db:5432/ShopDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    category = Column(String)
    quantity_in_stock = Column(Integer)


class Buyers(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    budget = Column(Integer)
    hashed_password = Column(String)


class Basket(Base):
    __tablename__ = 'basket'
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)

    buyer = relationship("Buyers", backref="cart_items")
    product = relationship("Products", backref="cart_items")
