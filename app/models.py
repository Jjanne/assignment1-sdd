from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class CoffeeShop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    lat: float
    lng: float
    is_cyclist_friendly: bool = True
    notes: Optional[str] = None

class GroupRide(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    date_time: datetime
    pace: str
    distance_km: float
    start_lat: float
    start_lng: float
    coffee_shop_id: Optional[int] = Field(default=None, foreign_key="coffeeshop.id")
