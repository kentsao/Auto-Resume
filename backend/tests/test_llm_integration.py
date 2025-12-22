"""Tests for LLM integration in endpoints."""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


@pytest.fixture
def mock_github_data():
    """Sample GitHub resume data."""
    return {
        "basics": {
            "name": "Test User",
            "summary": "A passionate software engineer with experience in Python and web development.",
            "email": "test@example.com"
        },
        "projects": [
            {
                "name": "Auto-Resume",
                "description": "An automated resume generator that fetches data from GitHub and creates beautiful resumes.",
                "url": "https://github.com/testuser/auto-resume",
                "languages": ["Python", "JavaScript"]
            }
        ]
    }


@pytest.fixture
def mock_summarizer():
    """Mock LLM summarizer."""
    mock = AsyncMock()
    mock.summarize_text = AsyncMock(side_effect=lambda text, category, audience="a recruiter": f"Summarized: {text[:30]}...")
    return mock


@patch('backend.app.main.generate_resume_from_github')
@patch('backend.app.main.get_summarizer')
def test_generate_resume_summarized_success(mock_get_summarizer, mock_generate, mock_github_data, mock_summarizer):
    """Test generating resume with LLM summarization."""
    mock_generate.return_value = mock_github_data
    mock_get_summarizer.return_value = mock_summarizer
    
    response = client.get("/generate/testuser/summarized?format=formal")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    
    # Verify summarizer was called
    assert mock_summarizer.summarize_text.called


@patch('backend.app.main.generate_resume_from_github')
@patch('backend.app.main.get_summarizer')
def test_generate_resume_summarized_with_token(mock_get_summarizer, mock_generate, mock_github_data, mock_summarizer):
    """Test generating resume with authentication token."""
    mock_generate.return_value = mock_github_data
    mock_get_summarizer.return_value = mock_summarizer
    
    response = client.get("/generate/testuser/summarized?token=test_token&format=ui")
    
    assert response.status_code == 200
    # Verify generate was called with token
    mock_generate.assert_called()


@patch('backend.app.main.generate_resume_from_github')
@patch('backend.app.main.get_summarizer')
def test_generate_resume_summarized_llm_failure(mock_get_summarizer, mock_generate, mock_github_data):
    """Test that endpoint continues when LLM fails."""
    mock_generate.return_value = mock_github_data
    
    # Make summarizer raise an error
    mock_summarizer = AsyncMock()
    mock_summarizer.summarize_text = AsyncMock(side_effect=Exception("LLM API error"))
    mock_get_summarizer.return_value = mock_summarizer
    
    # Should still succeed with unsummarized data
    response = client.get("/generate/testuser/summarized")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


@patch('backend.app.main.generate_resume_from_github')
def test_generate_resume_summarized_github_failure(mock_generate):
    """Test handling GitHub API failure."""
    mock_generate.side_effect = Exception("GitHub API error")
    
    response = client.get("/generate/testuser/summarized")
    
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_summarizer_integration():
    """Test that summarizer correctly processes resume data."""
    from backend.app.llm.summarizer import get_summarizer
    
    with patch('backend.app.llm.summarizer.GeminiSummarizer') as MockSummarizer:
        mock_instance = MockSummarizer.return_value
        mock_instance.summarize_text = AsyncMock(return_value="Brief summary")
        
        summarizer = get_summarizer()
        result = await summarizer.summarize_text("Long text here", "summary", "a recruiter")
        
        assert result == "Brief summary"
        mock_instance.summarize_text.assert_called_once_with("Long text here", "summary", "a recruiter")
