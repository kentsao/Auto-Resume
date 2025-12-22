# backend/app/db/crud.py
from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas


# User CRUD operations
def get_user_by_github_id(db: Session, github_id: int) -> Optional[models.User]:
    """Get user by GitHub ID."""
    return db.query(models.User).filter(models.User.github_id == github_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by GitHub username."""
    return db.query(models.User).filter(models.User.username == username).first()


def create_or_update_user(db: Session, user_data: dict) -> models.User:
    """Create a new user or update existing user from GitHub OAuth."""
    db_user = get_user_by_github_id(db, github_id=user_data["github_id"])
    
    if db_user:
        # Update existing user
        db_user.username = user_data["username"]
        db_user.email = user_data.get("email")
        db_user.name = user_data.get("name")
        db_user.avatar_url = user_data.get("avatar_url")
        db_user.bio = user_data.get("bio")
        db_user.access_token = user_data["access_token"]
    else:
        # Create new user
        db_user = models.User(**user_data)
        db.add(db_user)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# Resume CRUD operations
def get_resume_by_username(db: Session, username: str):
    return db.query(models.Resume).filter(models.Resume.github_username == username).first()


def create_or_update_resume(db: Session, resume: schemas.ResumeCreate):
    db_resume = get_resume_by_username(db, username=resume.github_username)
    if db_resume:
        # Update existing resume
        db_resume.resume_data = resume.resume_data
    else:
        # Create new resume
        db_resume = models.Resume(
            github_username=resume.github_username,
            resume_data=resume.resume_data
        )
        db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def delete_resume_by_username(db: Session, username: str):
    db_resume = get_resume_by_username(db, username=username)
    if db_resume:
        db.delete(db_resume)
        db.commit()
    return db_resume
