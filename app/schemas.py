from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CoffeeShopCreate(BaseModel):
    name: str
    address: str
    start_location: str
    is_cyclist_friendly: bool = True
    notes: Optional[str] = None

class CoffeeShopRead(CoffeeShopCreate):
    id: int

class GroupRideCreate(BaseModel):
    title: str
    date_time: datetime
    pace: str
    distance_km: float
    start_location: str
    coffee_shop_id: Optional[int] = None
    notes: Optional[str] = None

class GroupRideRead(GroupRideCreate):
    id: int
