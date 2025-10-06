# backend/tests/test_main.py
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.github_client.github_api import GITHUB_API_URL

client = TestClient(app)

@pytest.fixture
def mock_github_api():
    username = "kentsao"
    user_data = {
        "login": username,
        "name": "Kent Sao",
        "bio": "Backend engineer",
        "avatar_url": "https://example.com/kentsao.jpg",
        "html_url": f"https://github.com/{username}",
        "email": "kentsao@example.com",
    }
    repos_data = [
        {
            "name": "auto-resume",
            "description": "Resume generator",
            "html_url": f"https://github.com/{username}/auto-resume",
            "owner": {"avatar_url": "https://example.com/kentsao.jpg"},
            "fork": False,
            "languages_url": f"{GITHUB_API_URL}/repos/{username}/auto-resume/languages",
        }
    ]
    languages_data = {"Python": 123, "JavaScript": 456}

    with respx.mock as mock:
        mock.get(f"{GITHUB_API_URL}/users/{username}").mock(return_value=Response(200, json=user_data))
        mock.get(f"{GITHUB_API_URL}/users/{username}/repos").mock(return_value=Response(200, json=repos_data))
        mock.get(f"{GITHUB_API_URL}/repos/{username}/auto-resume/languages").mock(return_value=Response(200, json=languages_data))
        yield

def test_generate_resume_ui(mock_github_api):
    response = client.get("/generate/kentsao/ui")
    assert response.status_code == 200
    assert "Kent Sao" in response.text
    assert "auto-resume" in response.text

def test_generate_resume_formal(mock_github_api):
    response = client.get("/generate/kentsao/formal")
    assert response.status_code == 200
    assert "Kent Sao" in response.text
    assert "auto-resume" in response.text

def test_generate_resume_pdf(mock_github_api):
    response = client.get("/generate/kentsao/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=kentsao_resume.pdf" in response.headers["content-disposition"]