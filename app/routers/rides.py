from typing import Optional
from datetime import date, datetime, time, timedelta
from fastapi import Query, APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import GroupRide
from ..schemas import GroupRideCreate, GroupRideRead

# All endpoints related to group rides are here.
# Design notes:
# - `pace` is free text (e.g., "easy", "moderate", "fast") to keep inputs realistic.
# - `start_location` is human-friendly text (meeting spot), not coordinates.
# - We proactively validate coffee_shop_id so we don't create rides pointing to nowhere.

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("", response_model=GroupRideRead, status_code=201)
def create_ride(data: GroupRideCreate):
    """
    Create a new group ride.

    Why we validate coffee_shop_id here:
    - SQLite won't enforce foreign keys unless configured.
    - Even if it did, returning a friendly 400 with context is nicer for clients.
    """
    ride = GroupRide(**data.model_dump())
    with Session(engine) as session:
        # If a coffee shop is referenced, make sure it exists.
        if ride.coffee_shop_id is not None:
            from ..models import CoffeeShop  # lazy import keeps file-local concerns local
            if session.get(CoffeeShop, ride.coffee_shop_id) is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid coffee_shop_id: the referenced coffee shop does not exist."
                )
        session.add(ride)
        session.commit()
        session.refresh(ride)  # return the fresh row with id populated
    return ride


@router.get("", response_model=list[GroupRideRead])
def list_rides(pace: Optional[str] = Query(None), on_date: Optional[date] = Query(None)):
    """
    List rides with optional filters.

    Date filtering note:
    - Avoid calling .date() inside the SQL expression. SQLite can't translate that cleanly.
    - Instead, we build [start_of_day, next_day) bounds and compare datetimes.
    """
    with Session(engine) as session:
        stmt = select(GroupRide)

        if pace:
            # Exact match by design; simple and predictable for now.
            stmt = stmt.where(GroupRide.pace == pace)

        if on_date:
            # Build an inclusive/exclusive window for the calendar day.
            start_dt = datetime.combine(on_date, time(0, 0, 0))
            end_dt = start_dt + timedelta(days=1)
            stmt = stmt.where((GroupRide.date_time >= start_dt) & (GroupRide.date_time < end_dt))

        return session.exec(stmt).all()


@router.get("/{ride_id}", response_model=GroupRideRead)
def get_ride(ride_id: int):
    """Return one ride or a clear 404 if it doesn't exist."""
    with Session(engine) as session:
        ride = session.get(GroupRide, ride_id)
        if not ride:
            raise HTTPException(404, "Ride not found")
        return ride


@router.put("/{ride_id}", response_model=GroupRideRead)
def update_ride(ride_id: int, data: GroupRideCreate):
    """
    Full update (PUT) of a ride.

    Implementation detail:
    - We only set fields provided in the payload (`exclude_unset=True`),
      which keeps this idempotent and avoids wiping fields unintentionally.
    - We re-run coffee_shop_id validation to prevent dangling references after updates.
    """
    with Session(engine) as session:
        ride = session.get(GroupRide, ride_id)
        if not ride:
            raise HTTPException(404, "Ride not found")

        if data.coffee_shop_id is not None:
            from ..models import CoffeeShop
            if session.get(CoffeeShop, data.coffee_shop_id) is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid coffee_shop_id: the referenced coffee shop does not exist."
                )

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(ride, k, v)

        session.add(ride)
        session.commit()
        session.refresh(ride)
        return ride


@router.delete("/{ride_id}")
def delete_ride(ride_id: int):
    """
    Delete a ride. We return a small confirmation payload
    so clients can show a toast/snackbar without guessing.
    """
    with Session(engine) as session:
        ride = session.get(GroupRide, ride_id)
        if not ride:
            raise HTTPException(404, "Ride not found")
        session.delete(ride)
        session.commit()
    return {"ok": True, "message": "Ride deleted successfully."}
