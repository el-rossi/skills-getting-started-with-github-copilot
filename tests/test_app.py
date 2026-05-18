from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert "Programming Class" in body
    assert isinstance(body["Chess Club"], dict)


def test_signup_for_activity_adds_participant(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_duplicated_email_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity(client):
    email = "michael@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_400(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in activity"
