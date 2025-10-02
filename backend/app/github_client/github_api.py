import requests
from typing import List, Dict

GITHUB_API_URL = "https://api.github.com"


def fetch_user(username: str) -> Dict:
    """
    Fetch GitHub user profile and map to resume schema basics.
    """
    url = f"{GITHUB_API_URL}/users/{username}"
    resp = requests.get(url)
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


def fetch_repos(username: str) -> List[Dict]:
    """
    Fetch GitHub repos and map to resume schema projects.
    """
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    resp = requests.get(url)
    resp.raise_for_status()
    repos = resp.json()

    projects = []
    for repo in repos:
        projects.append({
            "name": repo.get("name", ""),
            "description": repo.get("description", ""),
            "url": repo.get("html_url", ""),
            "startDate": repo.get("created_at", ""),
            "endDate": repo.get("updated_at", ""),
            "roles": ["Contributor"],  # default role
            "image": repo.get("owner", {}).get("avatar_url", "")
        })
    return projects


def generate_resume_from_github(username: str) -> Dict:
    """
    Generate full resume JSON by combining user and repos.
    """
    resume = fetch_user(username)
    resume["projects"] = fetch_repos(username)
    return resume

if __name__ == "__main__":
    username = "your_account_name"
    resume = generate_resume_from_github(username)
    print(resume)