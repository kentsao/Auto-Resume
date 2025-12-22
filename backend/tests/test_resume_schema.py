import json
import pytest
from jsonschema import validate, ValidationError
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "app" / "models" / "resume_schema.json"
SAMPLE_PATH = Path(__file__).resolve().parent / "sample_resume.json"

# Load schema once
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    RESUME_SCHEMA = json.load(f)


def validate_resume(resume_json: dict):
    """Helper to validate resume JSON against schema"""
    validate(instance=resume_json, schema=RESUME_SCHEMA)


def test_sample_resume_is_valid():
    """The provided sample_resume.json should validate successfully"""
    with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
        sample_resume = json.load(f)
    validate_resume(sample_resume)  # should not raise

    # Optional: check image fields exist where expected
    basics_image = sample_resume["basics"].get("image")
    assert basics_image is not None and basics_image.strip() != "", "Author image is missing"

    for skill in sample_resume.get("skills", []):
        assert "image" in skill and skill["image"].strip() != "", f"Skill '{skill['name']}' image is missing"

    for project in sample_resume.get("projects", []):
        assert "image" in project and project["image"].strip() != "", f"Project '{project['name']}' image is missing"

    for work in sample_resume.get("work", []):
        assert "image" in work and work["image"].strip() != "", f"Work '{work.get('company', '')}' image is missing"

    for edu in sample_resume.get("education", []):
        assert "image" in edu and edu["image"].strip() != "", f"Education '{edu.get('institution', '')}' image is missing"


def test_invalid_resume_missing_required():
    """A resume missing required fields should fail validation"""
    bad_resume = {
        "basics": {"email": "oops@example.com"},
        "projects": []
    }
    with pytest.raises(ValidationError):
        validate_resume(bad_resume)


def test_invalid_email_format():
    """Email must be in proper format"""
    bad_resume = {
        "basics": {
            "name": "John Doe",
            "label": "Engineer",
            "email": "not-an-email",
            "summary": "This is a short summary"  # required in schema
        },
        "projects": []
    }
    with pytest.raises(ValidationError):
        validate_resume(bad_resume)
