from typing import Optional
from datetime import date
from fastapi import Query
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import GroupRide
from ..schemas import GroupRideCreate, GroupRideRead

router = APIRouter(prefix="/rides", tags=["rides"])

@router.post("", response_model=GroupRideRead)
def create_ride(data: GroupRideCreate):
    ride = GroupRide(**data.model_dump())
    with Session(engine) as session:
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
        if on_date:
            stmt = stmt.where(GroupRide.date_time.date() == on_date)
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
    return {"ok": True}
