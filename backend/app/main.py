# backend/app/main.py
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from backend.app.render.renderer import ResumeRenderer

app = FastAPI()

# Load sample resume data for preview
try:
    sample_resume_path = Path(__file__).parent.parent / "tests" / "sample_resume.json"
    with open(sample_resume_path, "r", encoding="utf-8") as f:
        resume_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    resume_data = {}  # Fallback to an empty dict if loading fails

@app.get("/preview/ui", response_class=HTMLResponse)
def preview_ui():
    renderer = ResumeRenderer(resume_data)
    return renderer.render_html(mode="ui")

@app.get("/preview/formal", response_class=HTMLResponse)
def preview_formal():
    renderer = ResumeRenderer(resume_data)
    return renderer.render_html(mode="formal")
