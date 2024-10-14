from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .auth import get_current_user
from ..database import SessionLocal, Buyers, Products

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
    quantity_in_stock: str


@router.get("/")
def read_all(db: Session = Depends(get_db), current_user: Buyers = Depends(get_current_user)):
    if current_user:
        items = db.query(Products).all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return items


@router.get("/{product_category}")
def find_by_category(product_category: str, db: Session = Depends(get_db),
                     current_user: Buyers = Depends(get_current_user)):
    if current_user:
        filter_category = db.query(Products).filter(Products.category == product_category).all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return filter_category


@router.post('/create')
def create_product(hello: ProductCreate, db: Session = Depends(get_db),
                   current_user: Buyers = Depends(get_current_user)):
    if current_user:
        hi = Products(**hello.dict())
        db.add(hi)
        db.commit()
        db.refresh(hi)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return hi


@router.put('/{tank}')
def put_product(put_id: int, bomba: ProductCreate, db: Session = Depends(get_db),
                current_user: Buyers = Depends(get_current_user)):
    if current_user:
        tank = db.query(Products).filter(Products.id == put_id).first()
        tank.name = bomba.name
        tank.description = bomba.description
        tank.price = bomba.price
        tank.category = bomba.category
        tank.quantity_in_stock = bomba.quantity_in_stock
        db.add(tank)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "Item updated", "item": tank}


@router.delete('/{del_id}')
def delete_item(del_id: int, db: Session = Depends(get_db), current_user: Buyers = Depends(get_current_user)):
    if current_user:
        car = db.query(Products).filter(Products.id == del_id).first()
        db.delete(car)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "Item deleted"}
