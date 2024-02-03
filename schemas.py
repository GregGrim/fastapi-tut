import datetime as dt
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(min_length=4, max_length=10)
    hashed_password: str = Field(min_length=4)
    full_name: str
    email: EmailStr | None = Field(default="example@email.com")
    phone_number: str


class UserSchema(BaseUser):
    id: int
    date_created: dt.datetime


class CreateUser(BaseUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
