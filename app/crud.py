from app import models, schemas
from app.auth import get_password_hash, decode_access_token
from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas import TokenData
from app.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.AuthRequest):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_access_token(token)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_transaction(db: Session, from_user_id: int, to_user_id: int, amount: int):
    sender = db.query(models.User).get(from_user_id)
    receiver = db.query(models.User).get(to_user_id)

    sender.coins -= amount
    receiver.coins += amount

    transaction = models.Transaction(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        amount=amount
    )
    db.add(transaction)
    db.commit()
    return {"message": "Coins transferred"}


def create_purchase(db: Session, user_id: int, item: str, price: int):
    user = db.query(models.User).get(user_id)
    user.coins -= price

    inventory_item = db.query(models.InventoryItem).filter(
        models.InventoryItem.owner_id == user_id,
        models.InventoryItem.item_type == item
    ).first()

    if inventory_item:
        inventory_item.quantity += 1
    else:
        inventory_item = models.InventoryItem(
            owner_id=user_id,
            item_type=item,
            quantity=1
        )
        db.add(inventory_item)

    db.commit()
    return {"message": f"Merch {item} bought"}


def add_coins(db: Session, user_id: int, coin_amount: int):
    user = db.query(models.User).get(user_id)

    user.coins += coin_amount
    db.commit()
    return {"message": f"Added {coin_amount} coin(s)"}
