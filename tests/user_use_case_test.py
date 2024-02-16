import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/users/signup")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/users/get/{username}")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_user():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/users/remove")
    assert response.status_code == 204
    assert response.json() is None


@pytest.mark.anyio
async def test_read_users_me():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/users/me")
    assert response.status_code == 200
