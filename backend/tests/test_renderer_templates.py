import pytest
from pathlib import Path
from backend.app.render.renderer import ResumeRenderer

@pytest.fixture
def sample_resume():
    return {
        "basics": {
            "name": "John Doe",
            "label": "Backend Engineer",
            "summary": "Passionate about building APIs and automation tools.",
            "image": "https://example.com/john.jpg"
        },
        "work": [
            {
                "company": "OpenAI",
                "position": "Backend Engineer",
                "startDate": "2023-01-01",
                "endDate": "2025-01-01",
                "summary": "Built scalable API systems.",
                "image": ""
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
                "image": ""
            }
        ],
        "skills": [
            {"name": "Python", "level": "Expert", "image": ""},
            {"name": "FastAPI", "level": "Advanced", "image": ""}
        ]
    }

def test_render_ui_html(tmp_path, sample_resume):
    renderer = ResumeRenderer(sample_resume)
    html_content = renderer.render_html(mode="ui")
    html_path = tmp_path / "resume_ui.html"
    html_path.write_text(html_content, encoding="utf-8")

    assert html_path.exists()
    assert "<h1>John Doe</h1>" in html_content
    assert "Backend Engineer" in html_content

def test_render_formal_pdf_and_html(tmp_path, sample_resume):
    renderer = ResumeRenderer(sample_resume)

    # Formal HTML
    formal_html = renderer.render_html(mode="formal")
    html_path = tmp_path / "resume_formal.html"
    html_path.write_text(formal_html, encoding="utf-8")
    assert html_path.exists()
    assert "<h1>John Doe</h1>" in formal_html

    # PDF output
    pdf_path = tmp_path / "resume_formal.pdf"
    pdf_bytes = renderer.render_pdf(mode="formal")
    pdf_path.write_bytes(pdf_bytes)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
