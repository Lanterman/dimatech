import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app, DOMAIN


auth_url = f"{DOMAIN}/auth"


# @pytest.mark.asyncio
# async def test_auth():
    # async with AsyncClient(transport=ASGITransport(app=app), base_url=auth_url) as ac:
        # correct_request = await ac.post("", data={"username": "test_user@mail.ru", "password": "stringstring"})
        # assert correct_request.status_code == 200, correct_request.status_code
        # response = correct_request.json()
        # assert False, correct_request
    #     incorrect_request = await ac.post("/auth", data={"username": "test_user@example.com", "password": "1234123412"})

    # assert correct_request.status_code == 202, correct_request.text
    # assert incorrect_request.status_code == 400, incorrect_request.text

    # response = correct_request.json()
    # incorrect_response = incorrect_request.json()
    # token.value = f"{response['type']} {response['access_token']}"
    # assert response["type"] == "Bearer", correct_request.text
    # assert incorrect_response["detail"] == "Incorrect email or password!"