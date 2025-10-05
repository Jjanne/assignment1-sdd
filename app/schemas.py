"""Pydantic schemas (request/response models) for validation and OpenAPI docs.

- Keep fields short and human-friendly (free-text `pace` and `start_location`).
- Use `*Read` models to include server-generated ids in responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CoffeeShopCreate(BaseModel):
    """Payload for creating/updating a coffee shop."""

    name: str = Field(min_length=1, max_length=100, description="Display name of the café")
    address: str = Field(min_length=1, max_length=200, description="Street address")
    # Human-friendly meeting point (e.g., “Retiro main gate”), not coordinates.
    start_location: str = Field(min_length=1, max_length=200, description="Landmark or meeting spot")
    is_cyclist_friendly: bool = True  # defaults to True; easy to toggle off
    notes: Optional[str] = Field(default=None, max_length=500, description="Optional free-form notes")


class CoffeeShopRead(CoffeeShopCreate):
    """Response model for a coffee shop row (includes id)."""

    id: int


class GroupRideCreate(BaseModel):
    """Payload for creating/updating a group ride."""

    title: str = Field(min_length=1, max_length=120, description="Ride title shown to riders")
    date_time: datetime  # ISO 8601 string in requests
    # Pace is intentionally free text so it matches how riders talk (“easy”, “moderate”, “spicy”).
    pace: str
    distance_km: float  # keep simple >0 validation in tests for now
    start_location: str = Field(min_length=1, max_length=200, description="Where we meet")
    coffee_shop_id: Optional[int] = None  # optional link; router validates existence
    notes: Optional[str] = Field(default=None, max_length=500, description="Optional ride notes")


class GroupRideRead(GroupRideCreate):
    """Response model for a ride row (includes id)."""

    id: int
