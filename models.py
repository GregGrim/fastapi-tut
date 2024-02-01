from pydantic import BaseModel

import datetime as dt
import sqlalchemy as sa

import database


class User(database.Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, index=True)
    full_name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, index=True, unique=True)
    phone_number = sa.Column(sa.String, index=True, unique=True)
    date_created = sa.Column(sa.DateTime, default=dt.datetime.utcnow())

