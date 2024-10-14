from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import Buyers, SessionLocal, Products, Basket

router = APIRouter(tags=['basket'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/buyers/{buyer_id}/basket")
def add_to_basket(buyer_id: int, product_id: int, quantity: int, db: Session = Depends(get_db),
                  current_user: Buyers = Depends(get_current_user)):
    if current_user:
        existing_item = db.query(Basket).filter_by(buyer_id=buyer_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = Basket(buyer_id=buyer_id, product_id=product_id, quantity=quantity)
            db.add(new_item)
        db.commit()
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
    basket_data = []
    for item in basket_items:
        product = db.query(Products).get(item.product_id)
        basket_data.append({
            "product_name": product.name,
            "product_id": product.id,
            "quantity": item.quantity,
            "price": product.price,
            "category": product.category,
            "description": product.description
        })
    return basket_data


@router.delete("/buyers/{buyer_id}/basket/{product_id}")
def remove_from_cart(buyer_id: int, product_id: int, quantity: int, db: Session = Depends(get_db),
                     current_user: Buyers = Depends(get_current_user)):
    if current_user.id != buyer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this basket")

    item_to_remove = db.query(Basket).filter_by(buyer_id=buyer_id, product_id=product_id).first()
    if item_to_remove is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in basket")

    if quantity == 0 or quantity >= item_to_remove.quantity:
        db.delete(item_to_remove)
    else:
        item_to_remove.quantity -= quantity
    db.commit()
    return {"message": "Item removed from basket"}
