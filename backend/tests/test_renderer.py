# backend/tests/test_renderer.py
import pytest
from backend.app.render.renderer import ResumeRenderer

@pytest.fixture
def sample_resume():
    return {
        "basics": {
            "name": "John Doe",
            "label": "Backend Engineer",
            "summary": "Building APIs and systems at scale",
            "image": "https://example.com/john.jpg"
        },
        "work": [
            {
                "company": "OpenAI",
                "position": "Backend Engineer",
                "startDate": "2023-01-01",
                "endDate": "2025-01-01",
                "summary": "Built scalable API systems.",
                "image": "https://example.com/work.jpg"
            }
        ],
        "projects": [
            {
                "name": "auto-resume",
                "description": "Resume generator project",
                "url": "https://github.com/johndoe/auto-resume",
                "startDate": "2025-01-01",
                "endDate": "2025-09-30",
                "image": "https://example.com/project.png"
            }
        ],
        "education": [
            {
                "institution": "MIT",
                "area": "Computer Science",
                "startDate": "2018-09-01",
                "endDate": "2022-06-30",
                "image": "https://example.com/mit.png"
            }
        ],
        "skills": [
            {"name": "Python", "level": "Expert", "image": "https://example.com/python.png"},
            {"name": "FastAPI", "level": "Advanced", "image": "https://example.com/fastapi.png"}
        ]
    }

def test_render_ui_html_sections(tmp_path, sample_resume):
    renderer = ResumeRenderer(sample_resume)
    html = renderer.render_html(mode="ui")
    html_path = tmp_path / "resume_ui.html"
    html_path.write_text(html, encoding="utf-8")

    assert html_path.exists()
    basics = sample_resume["basics"]
    assert basics["name"] in html
    assert basics["label"] in html
    assert "img" in html  # basics image rendered

    # Work section
    for work in sample_resume["work"]:
        assert work["company"] in html
        assert work["position"] in html
        assert work["summary"] in html

    # Projects section
    for project in sample_resume["projects"]:
        assert project["name"] in html
        assert project["description"] in html
        assert project["url"] in html
        assert project["image"] in html

    # Education section
    for edu in sample_resume["education"]:
        assert edu["institution"] in html
        assert edu["area"] in html
        assert edu["image"] in html

    # Skills section
    for skill in sample_resume["skills"]:
        assert skill["name"] in html
        assert skill["level"] in html
        assert skill["image"] in html

def test_render_formal_html_and_pdf(tmp_path, sample_resume):
    renderer = ResumeRenderer(sample_resume)

    # Formal HTML
    formal_html = renderer.render_html(mode="formal")
    html_path = tmp_path / "resume_formal.html"
    html_path.write_text(formal_html, encoding="utf-8")
    assert html_path.exists()
    assert sample_resume["basics"]["name"] in formal_html

    # PDF output
    pdf_path = tmp_path / "resume_formal.pdf"
    pdf_bytes = renderer.render_pdf(mode="formal")
    pdf_path.write_bytes(pdf_bytes)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
