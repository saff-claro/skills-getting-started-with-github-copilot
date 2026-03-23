def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    
    # Verify participant was added
    assert "newstudent@mergington.edu" in reset_activities["Chess Club"]["participants"]


def test_signup_duplicate_student(client, reset_activities):
    """Test that duplicate signup fails"""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_activity_full(client, reset_activities):
    """Test signup for activity at maximum capacity"""
    # Small Activity has max_participants=2 and 1 participant already
    response = client.post(
        "/activities/Small Activity/signup?email=student2@mergington.edu"
    )
    assert response.status_code == 200  # Should succeed, now at capacity
    
    # Next signup should fail
    response = client.post(
        "/activities/Small Activity/signup?email=student3@mergington.edu"
    )
    assert response.status_code == 400
    assert "maximum capacity" in response.json()["detail"]


def test_signup_multiple_students(client, reset_activities):
    """Test multiple different students can sign up"""
    student1 = "alice@mergington.edu"
    student2 = "bob@mergington.edu"
    
    response1 = client.post(f"/activities/Chess Club/signup?email={student1}")
    assert response1.status_code == 200
    
    response2 = client.post(f"/activities/Chess Club/signup?email={student2}")
    assert response2.status_code == 200
    
    assert student1 in reset_activities["Chess Club"]["participants"]
    assert student2 in reset_activities["Chess Club"]["participants"]
