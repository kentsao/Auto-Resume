import pytest
from unittest.mock import patch
from backend.app.github_client.github_api import fetch_user, fetch_repos

def test_fetch_user_maps_github_to_resume_fields():
    mock_response = {
        "login": "johndoe",
        "name": "John Doe",
        "bio": "Backend engineer",
        "avatar_url": "https://example.com/john.jpg",
        "blog": "https://johndoe.dev"
    }

    with patch("requests.get") as mock_get:
        class MockResponse:
            status_code = 200
            def json(self):
                return mock_response
            def raise_for_status(self):
                pass  # no-op, simulate successful status

        mock_get.return_value = MockResponse()

        result = fetch_user("johndoe")  # sync call

    basics = result["basics"]
    assert "name" in basics
    assert "summary" in basics
    assert "image" in basics
    assert basics["summary"] == mock_response["bio"]
    assert basics["image"] == mock_response["avatar_url"]

def test_fetch_repos_maps_github_repos_to_projects():
    mock_repos = [
        {
            "name": "auto-resume",
            "description": "Resume generator",
            "html_url": "https://github.com/johndoe/auto-resume",
            "owner": {"avatar_url": "https://example.com/john.jpg"}
        }
    ]

    with patch("requests.get") as mock_get:
        class MockResponse:
            status_code = 200
            def json(self):
                return mock_repos
            def raise_for_status(self):
                pass  # no-op

        mock_get.return_value = MockResponse()

        result = fetch_repos("johndoe")  # sync call

    assert isinstance(result, list)
    project = result[0]
    assert "name" in project
    assert "description" in project
    assert "url" in project
    assert "image" in project
