from hashlib import algorithms_available
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_exp_time: int

    class Config:
        env_file = ".env"


settings = Settings()
