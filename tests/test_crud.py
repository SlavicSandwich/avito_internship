import pytest
from tests.fixtures import db_session
from app.routers.items import MERCH_PRICES
from app.auth import verify_password, create_access_token
from app.crud import create_user, get_current_user, create_purchase, create_transaction, add_coins, get_user_by_username, get_user
import app.schemas as schemas

username = "username"
password = "password"

def test_get_user(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    assert user == get_user(db_session, user.id)

def test_get_user_by_username(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    assert user == get_user_by_username(db_session, username)

def test_create_user(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    assert user.username == username
    assert verify_password(password, user.password_hash) is True


def test_get_current_user(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    token = create_access_token({"sub": username})

    assert user == get_current_user(db_session, token)

def test_create_purchase(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    create_purchase(db_session, user.id, "cup", MERCH_PRICES["cup"])

    user = get_user_by_username(db_session, username)

    purchased_items = [{"item": purchase.item_type, "quantity": purchase.quantity} for purchase in user.inventory]

    assert purchased_items == [{"item": "cup", "quantity": 1}]


def test_create_transaction(db_session):
    sender = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    receiver = create_user(db_session, schemas.AuthRequest(
        username="receiver",
        password="receiver"
    ))

    create_transaction(db_session, sender.id, receiver.id, 100)

    sender = get_user_by_username(db_session, username)
    receiver = get_user_by_username(db_session, "receiver")

    sent_transactions = [
        {
            "fromUser": transaction.from_user_id,
            "toUser": transaction.to_user_id,
            "amount": transaction.amount
        } for transaction in sender.sent_transactions
    ]
    received_transactions = [
        {
            "fromUser": transaction.from_user_id,
            "toUser": transaction.to_user_id,
            "amount": transaction.amount
        } for transaction in receiver.received_transactions
    ]

    assert sent_transactions == [{"fromUser": 1, "toUser": 2, "amount": 100}]
    assert received_transactions == [{"fromUser": 1, "toUser": 2, "amount": 100}]

def test_add_coins(db_session):
    user = create_user(db_session, schemas.AuthRequest(
        username=username,
        password=password
    ))

    add_coins(db_session, user.id, 100)

    user = get_user_by_username(db_session, username)

    assert user.coins == 1100




