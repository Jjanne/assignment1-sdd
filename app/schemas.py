from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CoffeeShopCreate(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    is_cyclist_friendly: bool = True
    notes: Optional[str] = None

class CoffeeShopRead(CoffeeShopCreate):
    id: int

class GroupRideCreate(BaseModel):
    title: str
    date_time: datetime
    pace: str
    distance_km: float
    start_lat: float
    start_lng: float
    coffee_shop_id: Optional[int] = None

class GroupRideRead(GroupRideCreate):
    id: int
