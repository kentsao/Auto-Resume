"""GitHub OAuth2 authentication module."""
import os
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GitHubOAuthClient:
    """Handles GitHub OAuth2 authentication flow."""
    
    GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_USER_URL = "https://api.github.com/user"
    
    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/github/callback")
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set in environment variables. "
                "Register your app at https://github.com/settings/developers"
            )
    
    def get_authorization_url(self, state: str = None) -> str:
        """Generate GitHub authorization URL for login flow."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user:email,repo",  # Request email and repo access
            "state": state or "random_state_string"
        }
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.GITHUB_AUTHORIZE_URL}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GITHUB_TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri
                },
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = await response.json()
            
            if "error" in data:
                raise ValueError(f"GitHub OAuth error: {data.get('error_description')}")
            
            return data.get("access_token")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Fetch authenticated user information from GitHub."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GITHUB_USER_URL,
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            return await response.json()
    
    async def authenticate(self, code: str) -> Dict[str, Any]:
        """Complete OAuth flow: exchange code for token and fetch user info."""
        access_token = await self.exchange_code_for_token(code)
        user_info = await self.get_user_info(access_token)
        
        return {
            "access_token": access_token,
            "user": {
                "username": user_info.get("login"),
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "avatar_url": user_info.get("avatar_url"),
                "bio": user_info.get("bio")
            }
        }


def get_oauth_client() -> GitHubOAuthClient:
    """Factory function to get GitHub OAuth client."""
    return GitHubOAuthClient()
