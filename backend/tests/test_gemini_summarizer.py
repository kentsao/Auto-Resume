# backend/tests/test_gemini_summarizer.py
import pytest
import json
import os
from unittest.mock import patch, MagicMock

from backend.app.llm.summarizer import GeminiSummarizer


@pytest.fixture
def sample_resume_data():
    with open("backend/tests/sample_resume.json") as f:
        return json.load(f)

@pytest.fixture
def summarizer():
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        return GeminiSummarizer()

def test_init_with_no_api_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
            GeminiSummarizer()

@pytest.mark.asyncio
@patch('google.generativeai.GenerativeModel')
async def test_summarize_text(mock_model, summarizer):
    mock_response = MagicMock()
    mock_response.text = "Summarized text"
    mock_model.return_value.generate_content.return_value = mock_response

    summarizer.model = mock_model.return_value
    
    result = await summarizer.summarize_text("Some text", "category")
    
    summarizer.model.generate_content.assert_called_once_with("Please rephrase and summarize the following category information for a recruiter:\n\nSome text")
    assert result == "Summarized text"

@pytest.mark.asyncio
@patch('google.generativeai.GenerativeModel')
async def test_summarize_work_experience(mock_model, summarizer, sample_resume_data):
    mock_response = MagicMock()
    mock_response.text = "Summarized work experience"
    mock_model.return_value.generate_content.return_value = mock_response
    summarizer.model = mock_model.return_value

    work_item = sample_resume_data['work'][0]
    result = await summarizer.summarize_work_experience(work_item, "a recruiter")

    expected_input = f"Company: {work_item.get('company')}, Position: {work_item.get('position')}\nSummary: {work_item.get('summary')}\nHighlights: {', '.join(work_item.get('highlights', []))}"
    summarizer.model.generate_content.assert_called_once_with(f"Please rephrase and summarize the following work experience information for a recruiter:\n\n{expected_input}")
    assert result['summary'] == "Summarized work experience"
    assert result['company'] == work_item['company'] # Ensure other fields are untouched

@pytest.mark.asyncio
@patch('google.generativeai.GenerativeModel')
async def test_summarize_resume_data_work(mock_model, summarizer, sample_resume_data):
    mock_response = MagicMock()
    mock_response.text = "Summarized work item"
    mock_model.return_value.generate_content.return_value = mock_response
    summarizer.model = mock_model.return_value

    result = await summarizer.summarize_resume_data(sample_resume_data, "work")

    assert len(result['work']) == 1
    assert result['work'][0]['summary'] == "Summarized work item"
    assert summarizer.model.generate_content.call_count == 1

@pytest.mark.asyncio
@patch('google.generativeai.GenerativeModel')
async def test_summarize_resume_data_basics(mock_model, summarizer, sample_resume_data):
    mock_response = MagicMock()
    mock_response.text = "Summarized basics summary"
    mock_model.return_value.generate_content.return_value = mock_response
    summarizer.model = mock_model.return_value

    result = await summarizer.summarize_resume_data(sample_resume_data, "basics")

    assert result['basics']['summary'] == "Summarized basics summary"
    summarizer.model.generate_content.assert_called_once()
