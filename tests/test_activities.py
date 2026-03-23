def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Small Activity" in data


def test_get_activities_structure(client, reset_activities):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_participants(client, reset_activities):
    """Test that participants are correctly returned"""
    response = client.get("/activities")
    data = response.json()
    
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
    assert data["Programming Class"]["participants"] == ["emma@mergington.edu", "sophia@mergington.edu"]
