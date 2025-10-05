def _make_shop(client):
    r = client.post("/shops", json={
        "name": "Federal Café",
        "address": "Plaza",
        "start_location": "Lavapiés",
        "is_cyclist_friendly": True
    })
    assert r.status_code == 201
    return r.json()["id"]

def test_create_ride_valid_fk_and_filters(client):
    shop_id = _make_shop(client)

    # Create
    r = client.post("/rides", json={
        "title": "Evening Shakeout",
        "date_time": "2025-10-05T18:30:00",
        "pace": "easy",
        "distance_km": 8.5,
        "start_location": "Retiro Park main gate",
        "coffee_shop_id": shop_id,
        "notes": "Social pace."
    })
    assert r.status_code == 201
    ride_id = r.json()["id"]

    # List
    r = client.get("/rides")
    assert r.status_code == 200
    assert any(x["id"] == ride_id for x in r.json())

    # Filter by on_date 
    r = client.get("/rides", params={"on_date": "2025-10-05"})
    assert r.status_code == 200
    assert any(x["id"] == ride_id for x in r.json())

    # Get
    r = client.get(f"/rides/{ride_id}")
    assert r.status_code == 200

    # Update 
    r = client.put(f"/rides/{ride_id}", json={
        "title": "Evening Shakeout (revised)",
        "date_time": "2025-10-05T18:45:00",
        "pace": "moderate",
        "distance_km": 10.0,
        "start_location": "Retiro Park main gate",
        "coffee_shop_id": 1,
        "notes": "Longer loop."
    })
    assert r.status_code == 200
    assert r.json()["title"].endswith("(revised)")

    # Delete
    r = client.delete(f"/rides/{ride_id}")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_create_ride_invalid_fk_returns_400_with_message(client):
    # Invalid FK 
    r = client.post("/rides", json={
        "title": "Sunday Coffee Ride",
        "date_time": "2025-10-05T09:00:00",
        "pace": "moderate",
        "distance_km": 35.0,
        "start_location": "Temple of Debod",
        "coffee_shop_id": 9999
    })
    assert r.status_code == 400
    assert "does not exist" in r.json()["detail"]
