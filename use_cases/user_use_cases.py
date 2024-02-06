from fastapi import HTTPException
from entities import CreateUser, User, BaseUser
from repositories.cache_repository import CacheRepository
from repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, user_repo: UserRepository, cache_repo: CacheRepository):
        self.user_repo = user_repo
        self.cache_repo = cache_repo

    async def add_user(self, user: CreateUser):
        return await self.user_repo.create_one(user)

    async def get_user(self, username: str):
        user = await self.user_repo.get_one(username)
        if user is None:
            raise HTTPException(status_code=404, detail="user does not exist")
        return user

    async def delete_user(self, user: BaseUser):
        self.cache_repo.remove_all_user_tokens(user.id)
        await self.user_repo.delete_one(user)
        return {"details": "user successfully deleted"}
