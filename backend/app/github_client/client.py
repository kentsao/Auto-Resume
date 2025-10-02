import httpx

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.token = token
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"token {self.token}"}
        )

    async def get_repos(self, username: str):
        url = f"{self.BASE_URL}/users/{username}/repos"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
