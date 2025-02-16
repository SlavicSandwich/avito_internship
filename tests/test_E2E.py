import pytest
from tests.fixtures import client, db_session


def test_full_purchase_flow(client):
    auth_response = client.post("/api/auth", data={
        "username": "test_user_1",
        "password": "testpass"
    })
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    info_response = client.get("/api/info", headers=headers)
    assert info_response.status_code == 200
    initial_coins = info_response.json()["coins"]
    assert initial_coins == 1000

    buy_response = client.get("/api/buy/pen", headers=headers)
    assert buy_response.status_code == 200

    info_response = client.get("/api/info", headers=headers)
    assert info_response.status_code == 200
    assert {"type": "pen", "quantity": 1} in info_response.json()["inventory"]
    assert info_response.json()["coins"] == 990


def test_transfer_flow(client):
    sender_token = client.post("/api/auth", data={
        "username": "sender",
        "password": "testpass"
    }).json()['token']
    receiver_token = client.post("/api/auth", data={
        "username": "receiver",
        "password": "testpass"
    }).json()['token']

    sender_header = {"Authorization": f'Bearer {sender_token}'}
    receiver_header = {"Authorization": f'Bearer {receiver_token}'}

    transfer_response = client.post(
        "/api/sendCoin",
        headers=sender_header,
        json={
            "toUser": "receiver",
            "amount": 100
        }
    )
    assert transfer_response.status_code == 200

    sender_info = client.get("/api/info", headers=sender_header).json()
    receiver_info = client.get("/api/info", headers=receiver_header).json()

    assert sender_info == {
        'coins': 900,
        'inventory': [],
        'coinHistory':
            {
                'received': [],
                'sent':
                    [
                        {
                            'fromUser': 1,
                            'toUser': 2,
                            'amount': 100
                        }
                    ]
            }
    }
    assert receiver_info == {
        'coins': 1100,
        'inventory': [],
        'coinHistory':
            {
                'received':
                    [
                        {
                            'fromUser': 1,
                            'toUser': 2,
                            'amount': 100
                        }
                    ],
                'sent': []
            }
    }
