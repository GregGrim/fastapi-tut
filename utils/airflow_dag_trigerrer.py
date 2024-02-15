import base64
from uuid import uuid4
from settings import app_settings

import requests

# airflow uses basic (user:password) authorization
encoded_credentials = base64.b64encode(
    f"{app_settings.AIRFLOW_USER}:{app_settings.AIRFLOW_PASS}".encode()
).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json",
}


def trigger_dag(dag_id: str, config: dict):
    airflow_url = f"http://{app_settings.AIRFLOW_HOST}:{app_settings.AIRFLOW_PORT}/api/v1/dags/{dag_id}/dagRuns"

    payload = {"dag_run_id": str(uuid4()), "conf": config}
    response = requests.post(airflow_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        print(f"DAG {dag_id} triggered successfully.")
    else:
        print(f"Failed to trigger DAG {dag_id}. Error: {response.text}")
    return response.status_code
