import pytest
from app.auth import verify_password, create_access_token, decode_access_token, get_password_hash

password = "test_password"
fake_password = "fake_password"


def test_get_password_hash():
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password(fake_password, hashed) is False

def test_token():
    username = "user"
    token = create_access_token({"sub": username})
    decoded_username = decode_access_token(token)
    assert username == decoded_username

