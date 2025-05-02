from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DJANGO_SECRET_KEY: str = (
        "django-insecure-xz@_noicessisbjxrbs_ev)-1#!a2=*yhk&_$_%o7fa6vj&nwk"
    )

    DEBUG: bool = True

    BACKEND_ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]

    # database config
    POSTGRES_DATABASE: str = "concertos"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432


settings = Settings()
