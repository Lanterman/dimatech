import pytest

from httpx import AsyncClient, ASGITransport

from src.main import app, DOMAIN


user_url = f"{DOMAIN}/users"

@pytest.mark.asyncio
async def test_get_user_profile():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=user_url) as client:

        # No Auth
        response = await client.get(url="/profile")
        assert response.status_code == 401, response.status_code

        # Auth
        response