from fastapi.requests import Request

from entities import Token, User, CreateUserActivityLog
from exceptions import CredentialsException, LoginException, TokenDoesNotExistException
from repositories.log_repository import LogRepository
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from utils.crypto_utils import verify_sequence


class AuthUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: TokenRepository,
        log_repo: LogRepository,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.log_repo = log_repo

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.user_repo.get_one_by_username(username)
        if user and verify_sequence(
            source_sequence=password, target_sequence_hash=user.hashed_password
        ):
            return user

    def get_current_user(self, token: str) -> User:
        user_id = self.token_repo.read_access_token(token)
        user = self.user_repo.get_one(user_id)
        if user is None:
            raise CredentialsException()
        if not self.token_repo.token_exists(token, user.id):
            raise TokenDoesNotExistException()
        return user

    def login_user(self, username: str, password: str, request: Request) -> Token:
        user = self.authenticate_user(username, password)
        if not user:
            raise LoginException()
        self.log_repo.create_one(
            CreateUserActivityLog(
                message=f"User {username} logged in.",
                user_id=user.id,
                ipv4=request.client.host,
            )
        )
        access_token = self.token_repo.create_access_token(data={"sub": user.id})
        self.token_repo.add_token(access_token, user.id)
        return Token(access_token=access_token, token_type="bearer")

    def logout_user(self, token: str):
        self.token_repo.remove_token(token)
