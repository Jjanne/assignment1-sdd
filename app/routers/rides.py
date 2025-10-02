from typing import Optional
from datetime import date, datetime, time, timedelta
from fastapi import Query, APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import GroupRide
from ..schemas import GroupRideCreate, GroupRideRead

router = APIRouter(prefix="/rides", tags=["rides"])

@router.post("", response_model=GroupRideRead, status_code=201)
def create_ride(data: GroupRideCreate):
    ride = GroupRide(**data.model_dump())
    with Session(engine) as session:
        # Helpful error message if FK doesn't exist
        if ride.coffee_shop_id is not None:
            from ..models import CoffeeShop
            if session.get(CoffeeShop, ride.coffee_shop_id) is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid coffee_shop_id: the referenced coffee shop does not exist."
                )
        session.add(ride)
        session.commit()
        session.refresh(ride)
    return ride

@router.get("", response_model=list[GroupRideRead])
def list_rides(pace: Optional[str] = Query(None), on_date: Optional[date] = Query(None)):
    with Session(engine) as session:
        stmt = select(GroupRide)
        if pace:
            stmt = stmt.where(GroupRide.pace == pace)
        # Robust on_date filter using a day range (fixes the .date() issue)
        if on_date:
            start_dt = datetime.combine(on_date, time(0, 0, 0))
            end_dt = start_dt + timedelta(days=1)
            stmt = stmt.where((GroupRide.date_time >= start_dt) & (GroupRide.date_time < end_dt))
        return session.exec(stmt).all()

@router.get("/{ride_id}", response_model=GroupRideRead)
def get_ride(ride_id: int):
    with Session(engine) as session:
        ride = session.get(GroupRide, ride_id)
        if not ride:
            raise HTTPException(404, "Ride not found")
        return ride

@router.put("/{ride_id}", response_model=GroupRideRead)
def update_ride(ride_id: int, data: GroupRideCreate):
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
    with Session(engine) as session:
        ride = session.get(GroupRide, ride_id)
        if not ride:
            raise HTTPException(404, "Ride not found")
        session.delete(ride)
        session.commit()
    return {"ok": True, "message": "Ride deleted successfully."}
