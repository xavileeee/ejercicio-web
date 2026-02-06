import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update({
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
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })
    yield

client = TestClient(app)


def test_signup_success():
    r = client.post("/activities/Chess Club/signup", params={"email":"new@mergington.edu"})
    assert r.status_code == 200
    assert "Signed up new@mergington.edu for Chess Club" in r.json().get("message", "")
    assert "new@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_exact():
    r1 = client.post("/activities/Chess Club/signup", params={"email":"dup@mergington.edu"})
    assert r1.status_code == 200
    r2 = client.post("/activities/Chess Club/signup", params={"email":"dup@mergington.edu"})
    assert r2.status_code == 400
    assert "already signed up" in r2.json().get("detail", "")


def test_signup_duplicate_case_and_spaces():
    r1 = client.post("/activities/Chess Club/signup", params={"email":"case@mergington.edu"})
    assert r1.status_code == 200
    r2 = client.post("/activities/Chess Club/signup", params={"email":"  CASE@MERGINGTON.EDU  "})
    assert r2.status_code == 400
    assert "already signed up" in r2.json().get("detail", "")


def test_invalid_email():
    r = client.post("/activities/Chess Club/signup", params={"email":"invalid-email"})
    assert r.status_code == 400
    assert "Invalid email format" in r.json().get("detail", "")


def test_activity_not_found():
    r = client.post("/activities/Nonexistent/signup", params={"email":"a@b.com"})
    assert r.status_code == 404
