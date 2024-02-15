from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")
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
    AIRFLOW_PORT: str
    AIRFLOW_USER: str
    AIRFLOW_PASS: str
    AIRFLOW_HOST: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
app_settings = Settings()
