from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import GroupRide
from ..schemas import GroupRideCreate, GroupRideRead

router = APIRouter(prefix="/rides", tags=["rides"])

@router.post("", response_model=GroupRideRead)
def create_ride(data: GroupRideCreate):
    ride = GroupRide(**data.dict())
    with Session(engine) as session:
        session.add(ride)
        session.commit()
        session.refresh(ride)
    return ride

@router.get("", response_model=list[GroupRideRead])
def list_rides():
    with Session(engine) as session:
        return session.exec(select(GroupRide)).all()

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
        for k, v in data.dict().items():
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
