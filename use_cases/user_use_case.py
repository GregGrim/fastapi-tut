from entities import CreateUser
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from utils.airflow_dag_trigerrer import trigger_dag


class UserUseCase:
    def __init__(self, user_repo: UserRepository, cache_repo: TokenRepository):
        self.user_repo = user_repo
        self.cache_repo = cache_repo

    def add_user(self, user: CreateUser):
        return self.user_repo.create_one(user)

    def get_user(self, username: str):
        return self.user_repo.get_one_by_username(username)

    def delete_user(self, user_id: str):
        return trigger_dag(dag_id="remove_user_dag", config={"user_id": user_id})
