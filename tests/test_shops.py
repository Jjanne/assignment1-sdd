def test_shop_crud(client):
    # Create
    resp = client.post("/shops", json={
        "name": "La Bicicleta Café",
        "address": "Plaza de San Ildefonso, Madrid",
        "start_location": "Malasaña - plaza corner",
        "is_cyclist_friendly": True,
        "notes": "Big tables."
    })
    assert resp.status_code == 201
    shop = resp.json()
    shop_id = shop["id"]

    # List
    resp = client.get("/shops")
    assert resp.status_code == 200
    assert any(s["id"] == shop_id for s in resp.json())

    # Get
    resp = client.get(f"/shops/{shop_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "La Bicicleta Café"

    # Update
    resp = client.put(f"/shops/{shop_id}", json={
        "name": "La Bicicleta Café (Updated)",
        "address": "Plaza de San Ildefonso, Madrid",
        "start_location": "Malasaña - plaza corner",
        "is_cyclist_friendly": True,
        "notes": "Now with bike racks."
    })
    assert resp.status_code == 200
    assert resp.json()["name"].endswith("(Updated)")

    # Delete
    resp = client.delete(f"/shops/{shop_id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

    # 404 after delete
    resp = client.get(f"/shops/{shop_id}")
    assert resp.status_code == 404
