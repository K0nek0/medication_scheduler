import pytest

def test_create_schedule(test_client):
    response = test_client.post(
        "/api/v1/schedule",
        json={
            "user_id": 1,
            "name": "Test Medication",
            "frequency": "1 раз в день",
            "duration": 30
        }
    )
    assert response.status_code == 200
    assert "schedule_id" in response.json()

def test_get_schedule(test_client):
    create_response = test_client.post(
        "/api/v1/schedule",
        json={
            "user_id": 1,
            "name": "Test Medication",
            "frequency": "1 раз в день",
            "duration": 30
        }
    )
    schedule_id = create_response.json()["schedule_id"]
    
    response = test_client.get(
        f"/api/v1/schedule?user_id=1&schedule_id={schedule_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Medication"
    assert "schedule" in data
