from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    coins = Column(Integer, default=1000)

    inventory = relationship("InventoryItem", back_populates="owner")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_user_id")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_user_id")


class InventoryItem(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String)
    quantity = Column(Integer, default=1)
    owner = relationship("User", back_populates="inventory")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    to_user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)
