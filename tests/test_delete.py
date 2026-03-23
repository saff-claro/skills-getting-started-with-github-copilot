def test_delete_participant_success(client, reset_activities):
    """Test successful removal of a participant"""
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    
    # Verify participant was removed
    assert "michael@mergington.edu" not in reset_activities["Chess Club"]["participants"]


def test_delete_participant_not_found(client, reset_activities):
    """Test deletion of non-existent participant"""
    response = client.delete(
        "/activities/Chess Club/participants/notastudent@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_from_nonexistent_activity(client, reset_activities):
    """Test deletion from non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Club/participants/student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_then_signup_again(client, reset_activities):
    """Test that a removed participant can sign up again"""
    # Remove participant
    response1 = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Try to sign up again
    response2 = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response2.status_code == 200
    assert "michael@mergington.edu" in reset_activities["Chess Club"]["participants"]


def test_delete_multiple_participants(client, reset_activities):
    """Test deleting multiple participants"""
    initial_count = len(reset_activities["Chess Club"]["participants"])
    
    client.delete("/activities/Chess Club/participants/michael@mergington.edu")
    client.delete("/activities/Chess Club/participants/daniel@mergington.edu")
    
    final_count = len(reset_activities["Chess Club"]["participants"])
    assert final_count == initial_count - 2
