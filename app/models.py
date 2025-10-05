"""SQLModel ORM models for the Ride Planner domain.

Two tables:
- CoffeeShop: meeting places before or after rides.
- GroupRide: planned group sessions (optionally linked to a shop).
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class CoffeeShop(SQLModel, table=True):
    """A coffee shop cyclists like to meet at or finish at."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    # Human-friendly landmark or meeting point (“Retiro main gate”), not coordinates.
    start_location: str
    is_cyclist_friendly: bool = True
    # Free-form notes (bike racks, big tables, closing hours…)
    notes: Optional[str] = None


class GroupRide(SQLModel, table=True):
    """A planned group ride (title, time, pace, distance, start location)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    date_time: datetime
    # Kept as free text on purpose (e.g., "easy", "moderate", "fast").
    pace: str
    distance_km: float
    # Text meeting spot to keep data entry quick during planning.
    start_location: str
    # Optional link to a coffee shop. We still validate in the router for friendly errors.
    coffee_shop_id: Optional[int] = Field(default=None, foreign_key="coffeeshop.id")
    notes: Optional[str] = None
