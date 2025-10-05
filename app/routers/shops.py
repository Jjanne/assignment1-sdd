"""Coffee shop endpoints.

Design notes:
- Keep this router small and predictable: plain CRUD without filters.
- `start_location` is free text (meeting spot), which will be easier for cyclists to fill out.
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models import CoffeeShop
from ..schemas import CoffeeShopCreate, CoffeeShopRead

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("", response_model=CoffeeShopRead, status_code=201)
def create_shop(data: CoffeeShopCreate):
    """Create a coffee shop and return the freshly-inserted row (with id)."""
    shop = CoffeeShop(**data.model_dump())
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)  # refresh so the response includes the generated id
    return shop


@router.get("", response_model=list[CoffeeShopRead])
def list_shops():
    """Return all shops. Simple list—frontends can filter/sort client-side if needed."""
    with Session(engine) as session:
        return session.exec(select(CoffeeShop)).all()


@router.get("/{shop_id}", response_model=CoffeeShopRead)
def get_shop(shop_id: int):
    """Fetch one shop or respond with a clear 404."""
    with Session(engine) as session:
        shop = session.get(CoffeeShop, shop_id)
        if not shop:
            raise HTTPException(404, "Shop not found")
        return shop


@router.put("/{shop_id}", response_model=CoffeeShopRead)
def update_shop(shop_id: int, data: CoffeeShopCreate):
    """
    Update a shop in-place.

    Implementation detail:
    - We only set fields provided by the client (`exclude_unset=True`) so we don't
      accidentally blank out values on partial updates.
    """
    with Session(engine) as session:
        shop = session.get(CoffeeShop, shop_id)
        if not shop:
            raise HTTPException(404, "Shop not found")

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(shop, k, v)

        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop


@router.delete("/{shop_id}")
def delete_shop(shop_id: int):
    """Delete a shop and return a confirmation."""
    with Session(engine) as session:
        shop = session.get(CoffeeShop, shop_id)
        if not shop:
            raise HTTPException(404, "Shop not found")
        session.delete(shop)
        session.commit()
    return {"ok": True, "message": "Shop deleted successfully."}
