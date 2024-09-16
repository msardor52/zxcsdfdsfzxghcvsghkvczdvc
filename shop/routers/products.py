from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database import SessionLocal, Products

router = APIRouter(
    tags=['products'],
    prefix="/products"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    category: str


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    items = db.query(Products).all()
    return items


@router.get("/{product_category}")
def find_by_category(product_category: str, db: Session = Depends(get_db)):
    filter_category = db.query(Products).filter(Products.category == product_category).all()
    return filter_category


@router.post('/create')
def create_product(hello: ProductCreate, db: Session = Depends(get_db)):
    hi = Products(**hello.dict())
    db.add(hi)
    db.commit()
    db.refresh(hi)
    return hi


@router.put('/{tank}')
def put_product(put_id: int, bomba: ProductCreate, db: Session = Depends(get_db)):
    tank = db.query(Products).filter(Products.id == put_id).first()

    tank.name = bomba.name
    tank.description = bomba.description
    tank.price = bomba.price
    tank.category = bomba.category

    db.add(tank)
    db.commit()
    return {"message": "Item updated", "item": tank}


@router.delete('/{del_id}')
def delete_item(del_id: int, db: Session = Depends(get_db)):
    car = db.query(Products).filter(Products.id == del_id).first()
    db.delete(car)
    db.commit()
    return {"message": "Item deleted"}
