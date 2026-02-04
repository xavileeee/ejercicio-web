import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module

client = TestClient(app_module.app)

# Keep an original copy to restore before each test
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Restore the in-memory activities dict before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Clean up (not strictly necessary here)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "tester@example.com"
    res = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert res.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_duplicate():
    email = "duplicate@example.com"
    # First signup succeeds
    res1 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert res1.status_code == 200

    # Second signup fails with 400
    res2 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert res2.status_code == 400
    assert res2.json().get("detail") == "Student already signed up for this activity"


def test_signup_nonexistent_activity():
    res = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert res.status_code == 404


def test_delete_participant_success():
    email = "michael@mergington.edu"
    # Ensure the participant is present initially
    assert email in app_module.activities["Chess Club"]["participants"]

    res = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert res.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_delete_nonexistent_activity():
    res = client.delete("/activities/NoSuchActivity/participants?email=a@b.com")
    assert res.status_code == 404


def test_delete_not_signed_participant():
    email = "not-signed@example.com"
    # Ensure not present
    assert email not in app_module.activities["Chess Club"]["participants"]

    res = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert res.status_code == 400
    assert res.json().get("detail") == "Student not signed up for this activity"
