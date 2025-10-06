# backend/tests/test_github_api.py
import pytest
import respx
from httpx import Response

from backend.app.github_client.github_api import generate_resume_from_github, GITHUB_API_URL

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

@respx.mock
async def test_generate_resume_from_github_with_token():
    """Test that generate_resume_from_github correctly calls the GitHub API with a token."""
    username = "johndoe"
    token = "test_token"

    user_route = respx.get(f"{GITHUB_API_URL}/users/{username}").mock(return_value=Response(200, json={
        "login": "johndoe",
        "name": "John Doe",
        "bio": "Backend engineer",
        "avatar_url": "https://example.com/john.jpg",
        "html_url": "https://github.com/johndoe",
        "email": "johndoe@example.com",
    }))
    repos_route = respx.get(f"{GITHUB_API_URL}/users/{username}/repos").mock(return_value=Response(200, json=[
        {
            "name": "auto-resume",
            "description": "Resume generator",
            "html_url": "https://github.com/johndoe/auto-resume",
            "owner": {"avatar_url": "https://example.com/john.jpg"},
            "fork": False,
            "languages_url": f"{GITHUB_API_URL}/repos/johndoe/auto-resume/languages",
        }
    ]))
    languages_route = respx.get(f"{GITHUB_API_URL}/repos/johndoe/auto-resume/languages").mock(return_value=Response(200, json={"Python": 123, "JavaScript": 456}))

    await generate_resume_from_github(username, token=token)

    assert user_route.called
    assert repos_route.called
    assert languages_route.called
    assert user_route.calls.last.request.headers["authorization"] == f"token {token}"
    assert repos_route.calls.last.request.headers["authorization"] == f"token {token}"
    assert languages_route.calls.last.request.headers["authorization"] == f"token {token}"

@respx.mock
async def test_generate_resume_from_github_without_token():
    """Test that generate_resume_from_github correctly calls the GitHub API without a token."""
    username = "johndoe"

    user_route = respx.get(f"{GITHUB_API_URL}/users/{username}").mock(return_value=Response(200, json={
        "login": "johndoe",
        "name": "John Doe",
        "bio": "Backend engineer",
        "avatar_url": "https://example.com/john.jpg",
        "html_url": "https://github.com/johndoe",
        "email": "johndoe@example.com",
    }))
    repos_route = respx.get(f"{GITHUB_API_URL}/users/{username}/repos").mock(return_value=Response(200, json=[
        {
            "name": "auto-resume",
            "description": "Resume generator",
            "html_url": "https://github.com/johndoe/auto-resume",
            "owner": {"avatar_url": "https://example.com/john.jpg"},
            "fork": False,
            "languages_url": f"{GITHUB_API_URL}/repos/johndoe/auto-resume/languages",
        }
    ]))
    languages_route = respx.get(f"{GITHUB_API_URL}/repos/johndoe/auto-resume/languages").mock(return_value=Response(200, json={"Python": 123, "JavaScript": 456}))

    await generate_resume_from_github(username)

    assert user_route.called
    assert repos_route.called
    assert languages_route.called
    assert "authorization" not in user_route.calls.last.request.headers
    assert "authorization" not in repos_route.calls.last.request.headers
    assert "authorization" not in languages_route.calls.last.request.headers