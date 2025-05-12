import pytest
from datetime import time

@pytest.mark.asyncio
async def test_create_and_get_schedule(client, db_connection):
    test_data = {
        "schedule_id": 1,
        "user_id": 1,
        "name": "Test Schedule",
        "frequency": "daily",
        "duration": "30",
        "start_time": time(8, 0),
        "end_time": time(22, 0)
    }

    await db_connection.execute(
        """INSERT INTO schedules VALUES
        ($1, $2, $3, $4, $5, $6, $7)""",
        test_data["schedule_id"],
        test_data["user_id"],
        test_data["name"],
        test_data["frequency"],
        test_data["duration"],
        test_data["start_time"],
        test_data["end_time"]
    )

    response = client.get("/api/v1/schedule?user_id=1&schedule_id=1")
    assert response.status_code == 200
    
    result = response.json()
    assert result["name"] == "Test Schedule"
    assert result["frequency"] == "daily"