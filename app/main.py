from fastapi import FastAPI
from .database import init_db
from .routers import shops, rides

app = FastAPI(title="Ride Planner API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(shops.router)
app.include_router(rides.router)

@app.get("/")
def root():
    return {"service": "ride-planner", "status": "ok"}
