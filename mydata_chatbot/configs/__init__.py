from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"

    rdb_username: str = "username"
    rdb_password: str = "password"
    rdb_host: str = "0.0.0.0"
    rdb_db_name: str = "database"

    sqlite_url: str = "sqlite+aiosqlite:///sqlite3.db"

    # open ai
    openai_model: str = "gpt-3.5-turbo"
    openai_api_key: str = "openai_api_key"

    # tavily
    tavily_api_key: str | None = None


settings = Settings()
