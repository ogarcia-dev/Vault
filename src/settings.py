from decouple import config
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    
    # App config
    PROJECT_NAME: str = config("PROJECT_NAME", cast=str)
    PROJECT_VERSION: str = config("PROJECT_VERSION", cast=str)
    EXISTS_TABLES: bool = False

    # Database config
    DATABASE_URL: str = config("DATABASE_URL", cast=str)

    # Vault config
    VAULT_SECRET_KEY: str = config("VAULT_SECRET_KEY", cast=str)


    class Config:
        case_sensitive = True


SETTINGS = Settings()