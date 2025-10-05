"""FastAPI app bootstrap for the Ride Planner service.

- Use the FastAPI lifespan hook to initialize the SQLite schema on boot.
- Mount the two routers (shops, rides) so the OpenAPI groups are tidy.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import init_db
from .routers import shops, rides


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifecycle.
    - This runs once on startup (and once on shutdown).
    - We create tables up front so the first request doesn't race the DB.
    """
    init_db()
    yield
    # Nothing to tear down right now; SQLite file is local.


# A tiny bit of metadata helps when viewing /docs.
app = FastAPI(title="Ride Planner API", version="0.1.0", lifespan=lifespan)

# Grouped routes: they’ll show up as “shops” and “rides” tags in Swagger.
app.include_router(shops.router)
app.include_router(rides.router)


@app.get("/")
def root():
    """Lightweight health/info endpoint used by tests and uptime checks."""
    return {"service": "ride-planner", "status": "ok"}
