from fastapi import APIRouter, Depends, HTTPException
from app import schemas, crud, auth, models
from app.database import get_db
from sqlalchemy.orm import Session
from logging import getLogger, DEBUG

router = APIRouter(prefix="/api", tags=["users"])

logger = getLogger('uvicorn.error')
logger.setLevel(DEBUG)

@router.get("/info", response_model=schemas.InfoResponse)
def get_user_info(
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    user = crud.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # logger.debug('debug message')
    # logger.debug(user.received_transactions)
    # logger.debug(user.sent_transactions[0].from_user_id, user.sent_transactions[0].to_user_id)
    # logger.debug(user.sent_transactions[0].__dict__)
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

@router.post("/addCoin")
def add_coin(
        request: schemas.AddCoinRequest,
        current_user: models.User = Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    if request.amount < 0:
        raise HTTPException(400, detail="Can't add negative amount of coins")

    return crud.add_coins(db, current_user.id, request.amount)