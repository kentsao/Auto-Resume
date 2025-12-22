"""Tests for JWT utilities."""
import pytest
from datetime import timedelta
from backend.app.auth.jwt_utils import (
    create_access_token,
    verify_token,
    create_user_token,
    hash_password,
    verify_password
)


def test_create_access_token():
    """Test creating a JWT access token."""
    data = {"sub": "testuser", "github_id": 123}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_valid_token():
    """Test verifying a valid JWT token."""
    data = {"sub": "testuser", "github_id": 123, "email": "test@example.com"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    
    assert payload is not None
    assert payload["sub"] == "testuser"
    assert payload["github_id"] == 123
    assert payload["email"] == "test@example.com"
    assert "exp" in payload


def test_verify_invalid_token():
    """Test verifying an invalid JWT token."""
    invalid_token = "invalid.jwt.token"
    
    payload = verify_token(invalid_token)
    
    assert payload is None


def test_create_user_token():
    """Test creating a JWT token for a GitHub user."""
    token = create_user_token(
        username="testuser",
        github_id=12345,
        email="test@example.com"
    )
    
    assert token is not None
    
    payload = verify_token(token)
    assert payload["sub"] == "testuser"
    assert payload["github_id"] == 12345
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_create_user_token_without_email():
    """Test creating a user token without email."""
    token = create_user_token(
        username="testuser",
        github_id=12345
    )
    
    payload = verify_token(token)
    assert payload["sub"] == "testuser"
    assert payload["email"] is None


def test_token_expiration():
    """Test token with custom expiration."""
    data = {"sub": "testuser"}
    # Create token that expires in 1 second
    token = create_access_token(data, expires_delta=timedelta(seconds=1))
    
    # Token should be valid immediately
    payload = verify_token(token)
    assert payload is not None
    
    # Note: We can't easily test expiration without waiting or mocking time


def test_hash_password():
    """Test password hashing."""
    password = "my_secure_password123"
    hashed = hash_password(password)
    
    assert hashed is not None
    assert hashed != password
    assert len(hashed) > 0


def test_verify_password_correct():
    """Test verifying a correct password."""
    password = "my_secure_password123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test verifying an incorrect password."""
    password = "my_secure_password123"
    hashed = hash_password(password)
    
    assert verify_password("wrong_password", hashed) is False


def test_hash_password_different_hashes():
    """Test that same password produces different hashes (salt)."""
    password = "my_secure_password123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Hashes should be different due to salt
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
