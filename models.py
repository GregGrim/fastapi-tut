import datetime as dt
import sqlalchemy as sa

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, index=True, unique=True)
    hashed_password = sa.Column(sa.String, index=True)
    full_name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, index=True, unique=True)
    phone_number = sa.Column(sa.String, index=True, unique=True)
    date_created = sa.Column(sa.DateTime, default=dt.datetime.utcnow())

