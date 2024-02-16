from repositories.log_repository import LogRepository
from utils.airflow_dag_trigerrer import trigger_dag


class LogUseCase:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo

    def get_logs(self) -> list[dict]:
        logs = self.log_repo.get_all_logs()
        logs = [log.model_dump() for log in logs]
        return logs

    def send_logs(self, receiver_email: str):
        return trigger_dag(dag_id="send_logs_dag", config={"email": receiver_email})
