class GitHubClient:
    def __init__(self, token: str):
        self.token = token

    async def get_repos(self, username: str):
        # For now, return empty list (mock)
        return []
