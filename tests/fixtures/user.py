import pytest

from dependencies import get_user_use_case


@pytest.fixture
def user_use_case():
    return get_user_use_case()


@pytest.fixture
def create_user_data() -> dict:
    return {
        "username": "test",
        "hashed_password": "test",
        "full_name": "test",
        "email": "test@test.com",
        "phone_number": "+48000000000",
    }


@pytest.fixture
def user_id(user_use_case, create_user_data: dict) -> str | None:
    data = user_use_case.get_user(username=create_user_data["username"])
    if data:
        return data.id
