# backend/tests/test_github_client.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.app.github_client.github_api import fetch_user, fetch_repos

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_httpx_client():
    """Fixture to create a mock for httpx.AsyncClient."""
    mock_client = MagicMock(spec=AsyncMock)
    # The mock client's get method should be an awaitable mock
    mock_client.get = AsyncMock()
    return mock_client

async def test_fetch_user_maps_github_to_resume_fields(mock_httpx_client):
    """Test that fetch_user correctly calls the GitHub API and maps fields asynchronously."""
    mock_response_data = {
        "login": "johndoe",
        "name": "John Doe",
        "bio": "Backend engineer",
        "avatar_url": "https://example.com/john.jpg",
        "html_url": "https://github.com/johndoe",
        "email": "johndoe@example.com",
    }
    
    # Configure the mock response object that the async get call will return
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()

    mock_httpx_client.get.return_value = mock_response

    # Call the async function
    result = await fetch_user("johndoe", client=mock_httpx_client)

    # Assertions
    mock_httpx_client.get.assert_called_once_with(f"https://api.github.com/users/johndoe")
    basics = result["basics"]
    assert basics["name"] == "John Doe"
    assert basics["summary"] == "Backend engineer"
    assert basics["image"] == "https://example.com/john.jpg"

async def test_fetch_repos_maps_github_repos_to_projects(mock_httpx_client):
    """Test that fetch_repos correctly calls the GitHub API and maps fields asynchronously."""
    mock_repos_data = [
        {
            "name": "auto-resume",
            "description": "Resume generator",
            "html_url": "https://github.com/johndoe/auto-resume",
            "owner": {"avatar_url": "https://example.com/john.jpg"},
            "fork": False,
            "languages_url": "https://api.github.com/repos/johndoe/auto-resume/languages",
        }
    ]
    mock_languages_data = {"Python": 123, "JavaScript": 456}

    # Mock responses for repos and languages
    mock_repos_response = MagicMock()
    mock_repos_response.status_code = 200
    mock_repos_response.json.return_value = mock_repos_data
    mock_repos_response.raise_for_status = MagicMock()

    mock_languages_response = MagicMock()
    mock_languages_response.status_code = 200
    mock_languages_response.json.return_value = mock_languages_data
    mock_languages_response.raise_for_status = MagicMock()

    # Set side_effect to handle multiple get calls
    mock_httpx_client.get.side_effect = [mock_repos_response, mock_languages_response]

    # Call the async function
    result = await fetch_repos("johndoe", client=mock_httpx_client)

    # Assertions
    assert mock_httpx_client.get.call_count == 2
    mock_httpx_client.get.assert_any_call("https://api.github.com/users/johndoe/repos")
    mock_httpx_client.get.assert_any_call("https://api.github.com/repos/johndoe/auto-resume/languages")
    
    assert isinstance(result, list)
    project = result[0]
    assert project["name"] == "auto-resume"
    assert project["description"] == "Resume generator"
    assert project["languages"] == ["Python", "JavaScript"]