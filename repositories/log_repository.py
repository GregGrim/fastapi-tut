from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from entities import CreateUserActivityLog, UserActivityLog
from exceptions import LogCreationException
from models import LogModel


class LogRepository:
    def __init__(self, engine):
        self.engine = engine

    def create_one(self, log: CreateUserActivityLog) -> UserActivityLog:
        with Session(self.engine) as session:
            log_data = log.model_dump()
            log = LogModel(**log_data)
            try:
                session.add(log)
                session.commit()
            except SQLAlchemyError as e:
                error_message = (
                    str(e.__dict__["orig"]) if "orig" in e.__dict__ else str(e)
                )
                raise LogCreationException(
                    detail=f"Failed to create the log record: {error_message}"
                )
            session.refresh(log)
            return UserActivityLog.model_validate(log)

    def get_all_logs(self) -> list[UserActivityLog]:
        with Session(self.engine) as session:
            logs = session.query(LogModel).all()
            logs = [UserActivityLog.model_validate(log) for log in logs]
        return logs
