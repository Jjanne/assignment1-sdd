from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CoffeeShopCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=200)
    start_location: str = Field(min_length=1, max_length=200)
    is_cyclist_friendly: bool = True
    notes: Optional[str] = Field(default=None, max_length=500)

class CoffeeShopRead(CoffeeShopCreate):
    id: int

class GroupRideCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    date_time: datetime
    pace: str  
    distance_km: float
    start_location: str = Field(min_length=1, max_length=200)
    coffee_shop_id: Optional[int] = None
    notes: Optional[str] = Field(default=None, max_length=500)

class GroupRideRead(GroupRideCreate):
    id: int
