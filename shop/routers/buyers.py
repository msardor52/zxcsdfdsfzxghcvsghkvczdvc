from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database import SessionLocal, Buyers
from .auth import get_password_hash

router = APIRouter(
    tags=['buyers'],
    prefix="/buyers"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BuyerCreate(BaseModel):
    first_name: str
    last_name: str
    hashed_password: int
    nationality: str


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    people = db.query(Buyers).all()
    return people


@router.get("/{buyers_nationality}")
def find_by_nationality(buyers_nationality: str, db: Session = Depends(get_db)):
    filter_nationality = db.query(Buyers).filter(Buyers.nationality == buyers_nationality).all()
    return filter_nationality


@router.post('/create')
def create_buyer(something: BuyerCreate, db: Session = Depends(get_db)):
    anything = Buyers(**something.dict())
    db.add(anything)
    db.commit()
    db.refresh(anything)
    return anything


@router.put('/{rocket}')
def put_buyer(rocket: int, bomb: BuyerCreate, db: Session = Depends(get_db)):
    helicopter = db.query(Buyers).filter(Buyers.id == rocket).first()

    helicopter.first_name = bomb.first_name
    helicopter.last_name = bomb.last_name
    helicopter.hashed_password = bomb.hashed_password
    helicopter.nationality = bomb.nationality

    db.add(helicopter)
    db.commit()
    return {"message": "Item updated", "item": helicopter}


@router.delete('/{del_buyer}')
def delete_people(del_buyer: int, db: Session = Depends(get_db)):
    kamaz = db.query(Buyers).filter(Buyers.id == del_buyer).first()
    db.delete(kamaz)
    db.commit()
    return {"message": "Item deleted"}
