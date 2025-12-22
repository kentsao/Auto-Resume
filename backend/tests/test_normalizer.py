# backend/tests/test_normalizer.py
import pytest
from backend.app.normalizer.normalizer import DataNormalizer

@pytest.fixture
def sample_resume_data():
    return {
        "basics": {
            "name": "John Doe",
            "label": "Backend Engineer",
            "summary": "Building APIs and systems at scale",
            "image": "https://example.com/john.jpg"
        },
        "projects": [
            {
                "name": "auto-resume",
                "description": "Resume generator project",
                "url": "https://github.com/johndoe/auto-resume",
            }
        ],
    }

def test_data_normalizer(sample_resume_data):
    normalizer = DataNormalizer(sample_resume_data)
    normalized_data = normalizer.normalize()
    assert normalized_data == sample_resume_data
