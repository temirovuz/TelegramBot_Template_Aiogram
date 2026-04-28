from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Bot sozlamalari
    BOT_TOKEN: SecretStr
    ADMIN_ID: int

    # Database
    DB_URL: str

    # Ixtiyoriy sozlamalar
    BOT_NAME: str = "MyBot"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global instance
config = Settings()
