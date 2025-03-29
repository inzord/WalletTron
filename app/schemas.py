from pydantic import BaseModel
from typing import List
from datetime import date


class AddressRequestCreate(BaseModel):
    address: str


class AddressRequestResponse(BaseModel):
    id: int
    address: str
    bandwidth: float
    energy: float
    trx_balance: float
    time_created: date


class AddressRequestList(BaseModel):
    total: int
    items: List[AddressRequestResponse]
