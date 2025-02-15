from pydantic import BaseModel
from typing import List, Dict, Union

class TokenData(BaseModel):
    username: Union[str, None] = None

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str

class SendCoinRequest(BaseModel):
    toUser: str
    amount: int

class InventoryItem(BaseModel):
    type: str
    quantity: int

class TransactionHistory(BaseModel):
    fromUser: Union[str, None]
    toUser: str
    amount: int

class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: Dict[str, List[TransactionHistory]]