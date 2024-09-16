from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Buyers, Basket, SessionLocal
from .auth import get_current_user

router = APIRouter(tags=['basket'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/buyers/{buyer_id}/basket")
def add_to_basket(buyer_id: int, product_id: int, db: Session = Depends(get_db),
                  current_user: Buyers = Depends(get_current_user)):
    if current_user:
        new_item = Basket(buyer_id=buyer_id, product_id=product_id)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"message": "Added to basket"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


@router.get("/buyers/{buyer_id}/basket")
def show_basket(buyer_id: int, db: Session = Depends(get_db), current_user: Buyers = Depends(get_current_user)):
    buyer = db.query(Buyers).get(buyer_id)
    if buyer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")
    if current_user.id != buyer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this basket")

    basket_items = buyer.cart_items
    return [item.product for item in basket_items]


@router.delete("/buyers/{buyer_id}/basket/{product_id}")
def remove_from_cart(buyer_id: int, product_id: int, db: Session = Depends(get_db),
                     current_user: Buyers = Depends(get_current_user)):
    if current_user.id != buyer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this basket")

    item_to_remove = db.query(Basket).filter_by(buyer_id=buyer_id, product_id=product_id).first()
    if item_to_remove is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in basket")
    db.delete(item_to_remove)
    db.commit()
    return {"message": "Deleted"}

