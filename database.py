import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
import sqlalchemy.orm as orm

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/fastapi_db"

engine = sa.create_engine(DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
