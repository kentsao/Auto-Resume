# backend/app/github_client/github_api.py
import asyncio
import httpx
from typing import List, Dict, Any, Optional

GITHUB_API_URL = "https://api.github.com"

async def fetch_user(username: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """
    Fetch GitHub user profile asynchronously and map to resume schema basics.
    """
    url = f"{GITHUB_API_URL}/users/{username}"
    resp = await client.get(url)
    resp.raise_for_status()
    data = resp.json()

    basics = {
        "name": data.get("name", ""),
        "summary": data.get("bio", ""),
        "image": data.get("avatar_url", ""),
        "email": data.get("email", ""),
        "profiles": [
            {"network": "GitHub", "username": data.get("login", ""), "url": data.get("html_url", "")}
        ]
    }
    return {"basics": basics}

async def fetch_repo_languages(repo: Dict[str, Any], client: httpx.AsyncClient) -> List[str]:
    """Fetch repository languages."""
    languages_url = repo.get("languages_url")
    if not languages_url:
        return []
    
    resp = await client.get(languages_url)
    resp.raise_for_status()
    return list(resp.json().keys())

async def fetch_repos(username: str, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    """
    Fetch GitHub repos asynchronously and map to resume schema projects.
    """
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    resp = await client.get(url)
    resp.raise_for_status()
    repos = resp.json()

    # Concurrently fetch languages for all non-forked repos
    language_tasks = [fetch_repo_languages(repo, client) for repo in repos if not repo.get("fork")]
    all_languages = await asyncio.gather(*language_tasks)

    projects = []
    non_forked_repos = [repo for repo in repos if not repo.get("fork")]
    for i, repo in enumerate(non_forked_repos):
        projects.append({
            "name": repo.get("name", ""),
            "description": repo.get("description", ""),
            "url": repo.get("html_url", ""),
            "startDate": repo.get("created_at", ""),
            "endDate": repo.get("updated_at", ""),
            "roles": ["Contributor"],  # default role
            "image": repo.get("owner", {}).get("avatar_url", ""),
            "stargazers_count": repo.get("stargazers_count", 0),
            "languages": all_languages[i]
        })
    return projects


async def generate_resume_from_github(username: str, token: Optional[str] = None, client: Optional[httpx.AsyncClient] = None) -> Dict[str, Any]:
    """
    Generate full resume JSON by combining user and repos asynchronously.
    """
    headers = {"Authorization": f"token {token}"} if token else {}
    
    async def _generate(client: httpx.AsyncClient):
        user_data = await fetch_user(username, client)
        repo_data = await fetch_repos(username, client)
        resume = user_data
        resume["projects"] = repo_data
        return resume

    if client:
        return await _generate(client)
    else:
        async with httpx.AsyncClient(headers=headers) as client:
            return await _generate(client)