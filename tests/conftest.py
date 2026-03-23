import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Small Activity": {
            "description": "Test activity with small capacity",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["student1@mergington.edu"]
        }
    }
    
    # Clear existing activities and replace with initial state
    activities.clear()
    activities.update(initial_activities)
    
    yield activities
    
    # Cleanup after test
    activities.clear()
    activities.update(initial_activities)
