from fastapi import APIRouter, Depends, HTTPException
from app import schemas, crud, auth, models
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/info", response_model=schemas.InfoResponse)
def get_user_info(
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    user = crud.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {
        "coins": user.coins,
        "inventory": [
            {"type": item.item_type, "quantity": item.quantity}
            for item in user.inventory
        ],
        "coinHistory": {
            "received": [
                {"fromUser": t.from_user_id, "toUser": t.to_user_id, "amount": t.amount}
                for t in user.received_transactions
            ],
            "sent": [
                {"fromUser": t.from_user_id, "toUser": t.to_user_id, "amount": t.amount}
                for t in user.sent_transactions
            ]
        }
    }


@router.post("/sendCoin")
def send_coins(
        request: schemas.SendCoinRequest,
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    if request.amount <= 0:
        raise HTTPException(400, detail="Некорректная сумма")

    if current_user.coins < request.amount:
        raise HTTPException(400, detail="Недостаточно монет")

    receiver = crud.get_user_by_username(db, request.toUser)
    if not receiver:
        raise HTTPException(404, detail="Получатель не найден")

    return crud.create_transaction(
        db,
        from_user_id=current_user.id,
        to_user_id=receiver.id,
        amount=request.amount
    )