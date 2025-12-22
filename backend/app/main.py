# backend/app/main.py
import json
import uuid
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.render.renderer import ResumeRenderer
from backend.app.github_client.github_api import generate_resume_from_github
from backend.app.auth.github_oauth import get_oauth_client
from backend.app.auth.jwt_utils import create_user_token, verify_token
from backend.app.llm.summarizer import get_summarizer
from backend.app.db.database import engine, SessionLocal
from backend.app.db import models, crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user_optional(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        return None
    payload = verify_token(token)
    if not payload:
        return None
    username = payload.get("sub")
    if not username:
        return None
    return crud.get_user_by_username(db, username)

@app.get("/auth/github/login")
async def github_login():
    """Redirect user to GitHub authorization page."""
    try:
        oauth_client = get_oauth_client()
        state = str(uuid.uuid4())
        auth_url = oauth_client.get_authorization_url(state)
        # In production, store state in session/database for verification
        return RedirectResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/github/callback")
async def github_callback(code: str = Query(...), state: str = Query(None), db: Session = Depends(get_db)):
    """Handle GitHub OAuth callback and create JWT token."""
    try:
        oauth_client = get_oauth_client()
        auth_result = await oauth_client.authenticate(code)
        
        # Store user in database
        user_data = {
            "github_id": auth_result["user"].get("github_id", 0),  # Will need to fetch from GitHub API
            "username": auth_result["user"]["username"],
            "email": auth_result["user"].get("email"),
            "name": auth_result["user"].get("name"),
            "avatar_url": auth_result["user"].get("avatar_url"),
            "bio": auth_result["user"].get("bio"),
            "access_token": auth_result["access_token"]
        }
        
        # Create or update user in database
        db_user = crud.create_or_update_user(db, user_data)
        
        # Create JWT token
        jwt_token = create_user_token(
            username=db_user.username,
            github_id=db_user.github_id,
            email=db_user.email
        )
        
        # Redirect to frontend with token
        frontend_url = "http://localhost:5173/auth/callback"
        return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/test/ui", response_class=HTMLResponse)
async def test_resume_ui():
    """Render the ui.html template with sample data for testing."""
    try:
        with open("backend/tests/sample_resume.json") as f:
            resume_data = json.load(f)
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode="ui")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/{username}/ui", response_class=HTMLResponse)
async def generate_resume_ui(
    username: str, 
    token: str = None, 
    current_user: models.User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Generate a resume from GitHub and render it as an HTML UI."""
    try:
        if not token:
            # Only use stored token if the authenticated user matches the requested username
            if current_user and current_user.username == username and current_user.access_token:
                token = current_user.access_token

        resume_data = await generate_resume_from_github(username, token)
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode="ui")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/{username}/formal", response_class=HTMLResponse)
async def generate_resume_formal(
    username: str, 
    token: str = None, 
    current_user: models.User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Generate a resume from GitHub and render it as a formal HTML resume."""
    try:
        if not token:
            if current_user and current_user.username == username and current_user.access_token:
                token = current_user.access_token

        resume_data = await generate_resume_from_github(username, token)
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode="formal")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate/{username}/pdf")
async def generate_resume_pdf(
    username: str, 
    token: str = None, 
    current_user: models.User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Generate a resume from GitHub and render it as a PDF."""
    try:
        if not token:
            if current_user and current_user.username == username and current_user.access_token:
                token = current_user.access_token

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


@app.get("/generate/{username}/summarized", response_class=HTMLResponse)
async def generate_resume_summarized(
    username: str, 
    token: str = None, 
    format: str = "formal", 
    current_user: models.User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Generate a resume from GitHub, summarize with LLM, and render as HTML.
    
    Args:
        username: GitHub username
        token: Optional GitHub access token for private repos
        format: Output format ('formal' or 'ui', default: 'formal')
    """
    try:
        if not token:
            if current_user and current_user.username == username and current_user.access_token:
                token = current_user.access_token

        resume_data = await generate_resume_from_github(username, token)
        
        # Optional: Summarize using LLM
        try:
            summarizer = get_summarizer()
            # Summarize project descriptions
            if "projects" in resume_data:
                for project in resume_data["projects"]:
                    if project.get("description"):
                        project["description"] = await summarizer.summarize_text(
                            project["description"],
                            "project description"
                        )
            
            # Summarize bio/summary
            if "basics" in resume_data and resume_data["basics"].get("summary"):
                resume_data["basics"]["summary"] = await summarizer.summarize_text(
                    resume_data["basics"]["summary"],
                    "professional summary"
                )
        except Exception as llm_error:
            # If LLM fails, continue with unsummarized data
            print(f"LLM summarization failed (continuing without it): {llm_error}")
        
        renderer = ResumeRenderer(resume_data)
        return renderer.render_html(mode=format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
