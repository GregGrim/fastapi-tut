import time

import pytest
import requests

from entities import CreateUser, User
from use_cases.user_use_case import UserUseCase
from utils.airflow_dag_trigerrer import airflow_api, headers as airflow_auth_headers


def test_01_add_user(user_use_case: UserUseCase, create_user_data: dict):
    user = user_use_case.add_user(user=CreateUser(**create_user_data))
    assert isinstance(user, User)
    create_user_data.pop("hashed_password")
    assert all(
        getattr(user, prop) == create_user_data[prop] for prop in list(create_user_data)
    )


def test_02_get_user(user_use_case: UserUseCase, create_user_data):
    user = user_use_case.get_user(create_user_data["username"])
    assert isinstance(user, User)
    assert user.username == create_user_data["username"]


@pytest.mark.skip("Not stable")
def test_03_delete_user(user_use_case: UserUseCase, user_id, create_user_data):
    dag_run_data = user_use_case.delete_user(user_id=user_id)
    assert dag_run_data["status_code"] == 200
    dag_run_id = dag_run_data["dag_run_id"]
    for attempt in range(10):
        try:
            response = requests.get(
                f"{airflow_api}/dags/remove_user_dag/dagRuns/{dag_run_id}",
                headers=airflow_auth_headers,
            )
            assert response.json()["state"] == "success"
        except AssertionError:
            time.sleep(5)
    assert False, "Failed to delete user after 3 attempts"
