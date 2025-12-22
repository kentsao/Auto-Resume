"""Tests for GitHub OAuth authentication."""
import pytest
from unittest.mock import patch, AsyncMock
from backend.app.auth.github_oauth import GitHubOAuthClient, get_oauth_client


@pytest.fixture
def oauth_client():
    """Create an OAuth client with mocked environment variables."""
    with patch.dict('os.environ', {
        'GITHUB_CLIENT_ID': 'test_client_id',
        'GITHUB_CLIENT_SECRET': 'test_client_secret',
        'GITHUB_REDIRECT_URI': 'http://localhost:8000/auth/github/callback'
    }):
        return GitHubOAuthClient()


def test_oauth_client_initialization():
    """Test OAuth client initializes with required env vars."""
    with patch.dict('os.environ', {
        'GITHUB_CLIENT_ID': 'test_id',
        'GITHUB_CLIENT_SECRET': 'test_secret'
    }):
        client = GitHubOAuthClient()
        assert client.client_id == 'test_id'
        assert client.client_secret == 'test_secret'


def test_oauth_client_missing_credentials():
    """Test OAuth client raises error when credentials are missing."""
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError) as exc:
            GitHubOAuthClient()
        assert "GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET" in str(exc.value)


def test_get_authorization_url(oauth_client):
    """Test generating GitHub authorization URL."""
    state = "random_state_123"
    auth_url = oauth_client.get_authorization_url(state)
    
    assert "https://github.com/login/oauth/authorize" in auth_url
    assert "client_id=test_client_id" in auth_url
    assert "redirect_uri=" in auth_url
    assert "scope=user:email,repo" in auth_url
    assert f"state={state}" in auth_url


def test_get_authorization_url_default_state(oauth_client):
    """Test authorization URL with default state."""
    auth_url = oauth_client.get_authorization_url()
    assert "state=random_state_string" in auth_url


@pytest.mark.asyncio
async def test_exchange_code_for_token(oauth_client):
    """Test exchanging authorization code for access token."""
    mock_response = {
        "access_token": "test_access_token_123",
        "token_type": "bearer",
        "scope": "user:email,repo"
    }
    
    mock_response_obj = AsyncMock()
    mock_response_obj.json = AsyncMock(return_value=mock_response)
    
    with patch('backend.app.auth.github_oauth.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response_obj
        
        token = await oauth_client.exchange_code_for_token("test_code")
        assert token == "test_access_token_123"


@pytest.mark.asyncio
async def test_exchange_code_error_response(oauth_client):
    """Test handling GitHub OAuth error response."""
    mock_response = {
        "error": "bad_verification_code",
        "error_description": "The code passed is incorrect or expired."
    }
    
    mock_response_obj = AsyncMock()
    mock_response_obj.json = AsyncMock(return_value=mock_response)
    with patch('backend.app.auth.github_oauth.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response_obj
        with pytest.raises(ValueError) as exc:
            await oauth_client.exchange_code_for_token("invalid_code")
        assert "GitHub OAuth error" in str(exc.value)


@pytest.mark.asyncio
async def test_get_user_info(oauth_client):
    """Test fetching authenticated user information."""
    mock_user = {
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/123",
        "bio": "Software Engineer"
    }
    
    mock_response_obj = AsyncMock()
    mock_response_obj.json = AsyncMock(return_value=mock_user)
    with patch('backend.app.auth.github_oauth.httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response_obj
        user_info = await oauth_client.get_user_info("test_token")
        assert user_info == mock_user


@pytest.mark.asyncio
async def test_authenticate_full_flow(oauth_client):
    """Test complete OAuth authentication flow."""
    mock_token_response = {
        "access_token": "test_access_token",
        "token_type": "bearer"
    }
    
    mock_user_response = {
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/123",
        "bio": "Software Engineer"
    }
    
    mock_post_response = AsyncMock()
    mock_post_response.json = AsyncMock(return_value=mock_token_response)
    mock_get_response = AsyncMock()
    mock_get_response.json = AsyncMock(return_value=mock_user_response)
    with patch('backend.app.auth.github_oauth.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post, \
         patch('backend.app.auth.github_oauth.httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_post.return_value = mock_post_response
        mock_get.return_value = mock_get_response
        result = await oauth_client.authenticate("test_code")
        assert result["access_token"] == "test_access_token"
        assert result["user"]["username"] == "testuser"
        assert result["user"]["email"] == "test@example.com"


def test_get_oauth_client():
    """Test factory function returns GitHubOAuthClient instance."""
    with patch.dict('os.environ', {
        'GITHUB_CLIENT_ID': 'test_id',
        'GITHUB_CLIENT_SECRET': 'test_secret'
    }):
        client = get_oauth_client()
        assert isinstance(client, GitHubOAuthClient)
