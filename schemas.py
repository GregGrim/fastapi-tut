import datetime as dt
from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    full_name: str
    email: str
    phone_number: str


class User(BaseUser):
    id: int
    date_created: dt.datetime


class CreateUser(BaseUser):
    pass
