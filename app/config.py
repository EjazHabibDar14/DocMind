from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    groq_api_key: str = ''
    r2_account_id: str = ''
    r2_access_key_id: str = ''
    r2_secret_access_key: str = ''
    r2_bucket_name: str = ''

    class Config:
        env_file = '.env'

settings = Settings()