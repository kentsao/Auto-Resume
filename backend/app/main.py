# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from backend.app.render.renderer import ResumeRenderer
from backend.app.github_client.github_api import generate_resume_from_github

app = FastAPI()

@app.get("/generate/{username}/ui", response_class=HTMLResponse)
async def generate_resume_ui(username: str, token: str = None):
    """Generate a resume from GitHub and render it as an HTML UI."""
    try:
        resume_data = await generate_resume_from_github(username, token)
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode="ui")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/{username}/formal", response_class=HTMLResponse)
async def generate_resume_formal(username: str, token: str = None):
    """Generate a resume from GitHub and render it as a formal HTML resume."""
    try:
        resume_data = await generate_resume_from_github(username, token)
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode="formal")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/{username}/pdf")
async def generate_resume_pdf(username: str, token: str = None):
    """Generate a resume from GitHub and render it as a PDF."""
    try:
        resume_data = await generate_resume_from_github(username, token)
        renderer = ResumeRenderer(resume_data)
        pdf_bytes = renderer.render_pdf(mode="formal")
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={username}_resume.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
