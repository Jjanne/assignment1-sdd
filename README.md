# Ride Planner API (Assignment 1 – SD&D)

A minimal **FastAPI** application that manages **cycling group rides** and **coffee shops**.  
It uses REST API design, database persistence with SQLite, and clean modular structure.

---

## Setup & Run

# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure

assignment1-sdd/
│── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── database.py      # Database setup (SQLite + SQLModel engine)
│   ├── models.py        # ORM models (CoffeeShop, GroupRide)
│   ├── schemas.py       # Pydantic schemas for validation
│   └── routers/
│       ├── shops.py     # CoffeeShop endpoints
│       └── rides.py     # GroupRide endpoints
│── requests.http        # Example HTTP requests
│── requirements.txt     # Dependencies
│── README.md            # Documentation
│── REPORT.md            # SDLC choice and DevOps reflection
│── rideplanner.sqlite3  # SQLite database

---

## Architecture Design

classDiagram
    class CoffeeShop {
        +int id
        +str name
        +str address
        +str start_location
        +bool is_cyclist_friendly
        +str notes
    }

    class GroupRide {
        +int id
        +str title
        +datetime date_time
        +str pace
        +float distance_km
        +str start_location
        +int coffee_shop_id
        +str notes
    }

    CoffeeShop <|-- GroupRide : "linked by coffee_shop_id"

    class ShopRouter {
        +create_shop()
        +list_shops()
        +get_shop()
        +update_shop()
        +delete_shop()
    }

    class RideRouter {
        +create_ride()
        +list_rides(pace, on_date)
        +get_ride()
        +update_ride()
        +delete_ride()
    }

    ShopRouter --> CoffeeShop
    RideRouter --> GroupRide


---

## API Endpoints

### Coffee Shops
- `POST /shops` → Create a new coffee shop  
- `GET /shops` → List all coffee shops  
- `GET /shops/{id}` → Get details of a specific coffee shop  
- `PUT /shops/{id}` → Update a coffee shop 
- `DELETE /shops/{id}` → Delete a coffee shop

### Group Rides
- `POST /rides` → Create a new group ride  
- `GET /rides` → List all group rides (filters: pace, date)  
- `GET /rides/{id}` → Get details of a specific group ride
- `PUT /rides/{id}` → Update a ride
- `DELETE /rides/{id}` → Delete a ride

See REPORT.md for SDLC choice and DevOps reflection.
