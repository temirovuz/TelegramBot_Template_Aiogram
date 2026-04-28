# Konfiguratsiya hujjati

## Asosiy tamoyil

Barcha sozlamalar `.env` faylidan o'qiladi. Kod ichida hech qachon token, parol yoki ID qattiq yozilmaydi (hardcode).

`core/config.py` — bu sozlamalarni o'qib, validatsiya qiladigan yagona joy. Loyihaning istalgan joyida `from core.config import settings` yozib, kerakli qiymatni olish mumkin.

---

## `.env` fayli

```env
# ─── Bot ───────────────────────────────────────────
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ

# ─── Ma'lumotlar bazasi ────────────────────────────
# SQLite (oddiy, mahalliy ishlatish uchun)
DATABASE_URL=sqlite+aiosqlite:///data/bot.db

# PostgreSQL (production uchun tavsiya etiladi)
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/botdb

# ─── Admin ─────────────────────────────────────────
# Vergul bilan ajratilgan Telegram ID lar
ADMIN_IDS=123456789,987654321

# ─── Log ───────────────────────────────────────────
LOG_LEVEL=INFO
# Mumkin qiymatlar: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## `core/config.py` tuzilishi

```python
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Bot
    bot_token: str

    # Database
    database_url: str

    # Admin
    admin_ids: list[int] = []

    # Logging
    log_level: str = "INFO"

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: str | list) -> list[int]:
        if isinstance(v, str):
            return [int(i.strip()) for i in v.split(",") if i.strip()]
        return v


settings = Settings()
```

---

## O'zgaruvchilar jadvali

| O'zgaruvchi | Tur | Majburiy | Standart | Tavsif |
|---|---|---|---|---|
| `BOT_TOKEN` | `str` | ✅ | — | BotFather'dan olingan token |
| `DATABASE_URL` | `str` | ✅ | — | SQLAlchemy ulanish string'i |
| `ADMIN_IDS` | `list[int]` | ✅ | — | Vergul bilan ajratilgan admin ID'lari |
| `LOG_LEVEL` | `str` | ❌ | `INFO` | Loglash darajasi |

---

## Ishlatish misollari

```python
# istalgan faylda
from core.config import settings

# Bot token
token = settings.bot_token

# Admin tekshirish
if user_id in settings.admin_ids:
    ...

# DB URL
engine = create_async_engine(settings.database_url)
```

---

## Muhitga qarab sozlash

Agar bir necha muhit (local, staging, production) kerak bo'lsa:

```bash
# Local uchun
cp .env.example .env.local

# Production uchun
cp .env.example .env.production
```

```python
# core/config.py da
import os

env_file = os.getenv("ENV_FILE", ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file)
```

```bash
# Ishga tushirishda
ENV_FILE=.env.production uv run python main.py
```

---

## Xavfsizlik

- `.env` faylini **hech qachon** git'ga push qilmang
- `.gitignore` da quyidagilar bo'lishi shart:
  ```
  .env
  .env.*
  !.env.example
  ```
- Bot token'ini hech kim bilan ulashmang — agar siz bilan ulashilgan bo'lsa, darhol BotFather'da yangilang
- `ADMIN_IDS` ni minimal saqlang — haqiqatan admin kerak kishilarnigina qo'shing
