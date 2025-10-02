from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import init_db
from .routers import shops, rides

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Ride Planner API", version="0.1.0", lifespan=lifespan)

app.include_router(shops.router)
app.include_router(rides.router)

@app.get("/")
def root():
    return {"service": "ride-planner", "status": "ok"}
