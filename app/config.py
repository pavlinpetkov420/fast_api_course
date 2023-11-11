from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    App credentials class stored as environment variables.
    Pydantic provides us cast of values to pointed data type
    Env vars can be accessed as regular class attributes
    """
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
