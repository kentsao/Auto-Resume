import pytest
from backend.app.github_client.client import GitHubClient

@pytest.mark.asyncio
async def test_get_repos_returns_list():
    client = GitHubClient("fake-token")
    repos = await client.get_repos("fake-user")
    assert isinstance(repos, list)
