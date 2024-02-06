import datetime as dt

from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env')
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    JWT_ALGORITHM: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    # DATABASE_URL: PostgresDsn
    REDIS_PORT: str
    REDIS_HOST: str


settings = Settings()


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(min_length=4, max_length=10)
    hashed_password: str = Field(min_length=4)
    full_name: str
    email: EmailStr | None = Field(default="example@email.com")
    phone_number: str


class User(BaseUser):
    id: int
    date_created: dt.datetime


class CreateUser(BaseUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
