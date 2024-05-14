from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # sql-db settings
    sql_hostname: str = "localhost"
    sql_port: int = 5432
    sql_username: str
    sql_password: str
    sql_db_name: str

    # mongo-db settings
    mongo_hostname: str = "localhost"
    mongo_username: str
    mongo_password: str
    mongo_db_name: str
    mongo_videos_collection: str
    mongo_audios_collection: str

    # oauth settings
    oauth_secret_key: str
    oauth_algorithm: str
    oauth_expiry_minutes: int

    # rabbit settings
    rabbit_host: str = "localhost"
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_videos_queue: str
    rabbit_audios_queue: str

    class Config:
        env_file = ".env"


settings = Settings()
