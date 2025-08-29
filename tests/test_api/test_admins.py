import pytest

from httpx import ASGITransport, AsyncClient

from src.main import app, DOMAIN
from tests.test_data import user_info_1, user_info_2, token


admin_url = f"{DOMAIN}/admins"


@pytest.mark.asyncio
async def test_get_admin_info():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=admin_url) as ac:
        # No Auth
        request_1 = await ac.get("/profile")
        assert request_1.status_code == 401, request_1.text

        # request_2 = await ac.get("/profile", headers={"Authorization": f'Bearer {token.value}'})
        # incorrect_request = await ac.post("/sign-on", json=incorrect_user_info)

    # assert request_2.status_code == 201, request_2.text
    # assert incorrect_request.status_code == 406, incorrect_request.text

    # response_2 = request_2.json()
    # incorrect_response = incorrect_request.json()
    # assert response_2["gender"] == "Girl", request_2.text
