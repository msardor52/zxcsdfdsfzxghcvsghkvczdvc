from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi import status
from fastapi.testclient import TestClient
import pytest

from ..routers.products import get_db
from ..main import app
from ..database import Base, Products

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_products.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Products(
        name="hello",
        description="hello",
        price=5,
        category="hello",
        quantity_in_stock=5
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM products;"))
        connection.commit()


def test_read_all(test_todo):
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'description': 'hello', 'id': 1, 'name': 'hello', 'quantity_in_stock': 5, 'category': 'hello', 'price': 5}]


def test_read_one(test_todo):
    response = client.get("/products/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'description': 'hello', 'id': 1, 'name': 'hello',
                               'quantity_in_stock': 5, 'category': 'hello', 'price': 5}


def test_read_not_found(test_todo):
    response = client.get("/products/52355159")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "Product not found"}


def test_create_product(test_todo):
    request_data = {
        'description': 'hello',
        'name': 'hello',
        'quantity_in_stock': 5,
        'category': 'hello',
        'price': 5
    }

    response = client.post('/products/create', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Products).filter(Products.id == 2).first()
    assert model.name == request_data.get('name')
    assert model.description == request_data.get('description')
    assert model.price == request_data.get('price')
    assert model.category == request_data.get('category')
    assert model.quantity_in_stock == request_data.get('quantity_in_stock')


def test_update_products(test_todo):
    request_data = {
        'description': 'hello world',
        'name': 'hello world',
        'quantity_in_stock': 10,
        'category': 'hello world',
        'price': 10
    }

    response = client.put('products/put/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Products).filter(Products.id == 1).first()
    assert model.description == 'hello world'


def test_delete_todo(test_todo):
    response = client.delete("/products/delete/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Products).filter(Products.id == 1).first()
    assert model is None
