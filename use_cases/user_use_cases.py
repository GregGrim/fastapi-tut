from entities import CreateUser
from exceptions import UserDoesNotExistException
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, user_repo: UserRepository, cache_repo: TokenRepository):
        self.user_repo = user_repo
        self.cache_repo = cache_repo

    async def add_user(self, user: CreateUser):
        return await self.user_repo.create_one(user)

    async def get_user(self, username: str):
        user = await self.user_repo.get_one_by_username(username)
        if user is None:
            raise UserDoesNotExistException()
        return user

    async def delete_user(self, user_id: str):
        self.cache_repo.remove_all_user_tokens(user_id)
        await self.user_repo.delete_one(user_id)
