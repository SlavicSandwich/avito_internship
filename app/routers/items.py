from fastapi import APIRouter, Depends, HTTPException
from app import crud, auth, models
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["items"])

MERCH_PRICES = {
    "t-shirt": 80,
    "cup": 20,
    "book": 50,
    "pen": 10,
    "powerbank": 200,
    "hoody": 300,
    "umbrella": 200,
    "socks": 10,
    "wallet": 50,
    "pink-hoody": 500
}


@router.get("/buy/{item}")
def buy_item(
        item: str,
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    if item not in MERCH_PRICES:
        raise HTTPException(404, detail="Товар не найден")

    price = MERCH_PRICES[item]
    if current_user.coins < price:
        raise HTTPException(400, detail="Недостаточно монет")

    return crud.create_purchase(db, user_id=current_user.id, item=item, price=price)