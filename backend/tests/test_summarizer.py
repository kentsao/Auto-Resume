# backend/tests/test_summarizer.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from backend.app.llm.summarizer import get_summarizer, LLMSummarizer


@pytest.fixture
def sample_resume_data():
    return {
        "basics": {
            "summary": "This is a long summary that should be summarized."
        },
        "work": [
            {
                "company": "Test Company",
                "position": "Software Engineer",
                "summary": "Worked on various projects",
                "highlights": ["Achievement 1", "Achievement 2"]
            }
        ]
    }

@patch('backend.app.llm.summarizer.GeminiSummarizer')
def test_get_summarizer(MockGeminiSummarizer):
    mock_instance = MockGeminiSummarizer.return_value
    summarizer = get_summarizer()
    assert summarizer == mock_instance

@pytest.mark.asyncio
@patch('backend.app.llm.summarizer.GeminiSummarizer')
async def test_summarize_resume_data_call(MockGeminiSummarizer, sample_resume_data):
    mock_instance = MockGeminiSummarizer.return_value
    mock_instance.summarize_resume_data = AsyncMock(return_value=sample_resume_data)
    
    summarizer = get_summarizer()
    await summarizer.summarize_resume_data(sample_resume_data, category="basics")
    
    mock_instance.summarize_resume_data.assert_called_once_with(sample_resume_data, category="basics")

@pytest.mark.asyncio
@patch('backend.app.llm.summarizer.GeminiSummarizer')
async def test_summarize_text(MockGeminiSummarizer):
    mock_instance = MockGeminiSummarizer.return_value
    mock_instance.summarize_text = AsyncMock(return_value="Summarized text")
    
    summarizer = get_summarizer()
    result = await summarizer.summarize_text("Test text", "test category")
    
    mock_instance.summarize_text.assert_called_once_with("Test text", "test category")
    assert result == "Summarized text"

@pytest.mark.asyncio
@patch('backend.app.llm.summarizer.GeminiSummarizer')
async def test_summarize_work_experience(MockGeminiSummarizer, sample_resume_data):
    mock_instance = MockGeminiSummarizer.return_value
    work_item = sample_resume_data["work"][0]
    mock_instance.summarize_work_experience = AsyncMock(return_value=work_item)
    
    summarizer = get_summarizer()
    result = await summarizer.summarize_work_experience(work_item, "a recruiter")
    
    mock_instance.summarize_work_experience.assert_called_once_with(work_item, "a recruiter")
    assert result == work_item

@pytest.mark.asyncio
@patch('backend.app.llm.summarizer.GeminiSummarizer')
async def test_summarize_resume_data_work_category(MockGeminiSummarizer, sample_resume_data):
    mock_instance = MockGeminiSummarizer.return_value
    mock_instance.summarize_resume_data = AsyncMock(return_value=sample_resume_data)
    
    summarizer = get_summarizer()
    result = await summarizer.summarize_resume_data(sample_resume_data, category="work")
    
    mock_instance.summarize_resume_data.assert_called_once_with(sample_resume_data, category="work")
    assert result == sample_resume_data

@pytest.mark.asyncio
async def test_gemini_summarizer_initialization():
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        with patch('google.generativeai.configure') as mock_configure:
            from backend.app.llm.summarizer import GeminiSummarizer
            summarizer = GeminiSummarizer()
            mock_configure.assert_called_once_with(api_key='test_key')

@pytest.mark.asyncio
async def test_gemini_summarizer_missing_api_key():
    with patch.dict('os.environ', clear=True):
        from backend.app.llm.summarizer import GeminiSummarizer
        with pytest.raises(ValueError) as exc_info:
            summarizer = GeminiSummarizer()
        assert str(exc_info.value) == "GEMINI_API_KEY not found in environment variables. Please add it to your .env file."
