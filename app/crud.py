from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.AuthRequest):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
    return {"message": "Монеты успешно отправлены"}


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
    return {"message": f"Товар {item} успешно куплен"}