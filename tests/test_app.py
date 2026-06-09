from fastapi import status

from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, allow_redirects=False)

    # Assert
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    assert "Chess Club" in json_data
    assert json_data["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@mergington.edu"
    before_participants = list(activities[activity]["participants"])
    url = f"/activities/{activity}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == len(before_participants) + 1


def test_signup_for_same_student_returns_bad_request(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    url = f"/activities/{activity}/signup"

    # Act
    first_response = client.post(url, params={"email": email})
    second_response = client.post(url, params={"email": email})

    # Assert
    assert first_response.status_code == status.HTTP_200_OK
    assert second_response.status_code == status.HTTP_400_BAD_REQUEST
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    url = f"/activities/{activity}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity}/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Removed {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_remove_missing_participant_returns_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    url = f"/activities/{activity}/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found"
