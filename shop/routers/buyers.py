from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .auth import get_current_user
from ..database import Buyers, SessionLocal

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
    username: str
    budget: int
    hashed_password: str


@router.get("/")
def read_all(db: Session = Depends(get_db),):
    #          current_user: Buyers = Depends(get_current_user)):
    # if current_user:
    people = db.query(Buyers).all()
    # else:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return people


@router.get("/{buyers_id}")
def find_by_id(buyers_id: int, db: Session = Depends(get_db),):
                #current_user: Buyers = Depends(get_current_user)):
    #if current_user:
    filter_nationality = db.query(Buyers).filter(Buyers.id == buyers_id).first()
#    else:
 #       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return filter_nationality


@router.post('/create')
def create_buyer(something: BuyerCreate, db: Session = Depends(get_db),):
#                 current_user: Buyers = Depends(get_current_user)):
#    if current_user:
    anything = Buyers(**something.dict())
    db.add(anything)
    db.commit()
    db.refresh(anything)
#    else:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return anything


@router.put('/{rocket}')
def put_buyer(rocket: int, bomb: BuyerCreate, db: Session = Depends(get_db),):
    #           current_user: Buyers = Depends(get_current_user)):
    # if current_user:
    helicopter = db.query(Buyers).filter(Buyers.id == rocket).first()
    helicopter.username = bomb.username
    helicopter.hashed_password = bomb.hashed_password
    helicopter.budget = bomb.budget
    db.add(helicopter)
    db.commit()
    #else:
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "Item updated", "item": helicopter}


@router.delete('/{del_buyer}')
def delete_people(del_buyer: int, db: Session = Depends(get_db),):
                  #current_user: Buyers = Depends(get_current_user)):
    #if current_user:
    kamaz = db.query(Buyers).filter(Buyers.id == del_buyer).first()
    db.delete(kamaz)
    db.commit()
    #else:
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"message": "Item deleted"}
