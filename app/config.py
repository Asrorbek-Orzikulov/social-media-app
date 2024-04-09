from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # db settings
    db_hostname: str = "localhost"
    db_port: int = 5432
    db_username: str
    db_password: str
    db_name: str

    # oauth settings
    oauth_secret_key: str
    oauth_algorithm: str
    oauth_expiry_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
