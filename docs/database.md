# Ma'lumotlar bazasi hujjati

## Texnologiyalar

| Kutubxona | Maqsad |
|---|---|
| SQLAlchemy 2.x | ORM — Python orqali DB bilan ishlash |
| aiosqlite / asyncpg | Asinxron DB drayveri |
| Alembic | Migratsiyalar — jadval o'zgarishlarini kuzatish |

---

## Modellar (`db/models.py`)

Har bir jadval — alohida Python klassi.

```python
# db/models.py
from datetime import datetime
from sqlalchemy import BigInteger, String, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    full_name: Mapped[str] = mapped_column(String(256))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
```

---

## CRUD operatsiyalari (`db/crud.py`)

CRUD — Create, Read, Update, Delete. Bu faylda faqat DB so'rovlari bo'ladi, biznes mantiq yo'q.

```python
# db/crud.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


async def get_user(telegram_id: int, session: AsyncSession) -> User | None:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    telegram_id: int,
    username: str | None,
    full_name: str,
    session: AsyncSession,
) -> User:
    user = User(
        telegram_id=telegram_id,
        username=username,
        full_name=full_name,
    )
    session.add(user)
    await session.flush()   # ID ni olish uchun, lekin hali commit emas
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    return list(result.scalars().all())


async def update_user_ban(
    telegram_id: int,
    is_banned: bool,
    session: AsyncSession,
) -> User | None:
    user = await get_user(telegram_id, session)
    if user:
        user.is_banned = is_banned
        await session.flush()
    return user
```

---

## Session boshqaruvi

Session middleware orqali har bir so'rovda avtomatik ochiladi va yopiladi:

```python
# middlewares/ ichida (db_session middleware)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self.session_factory() as session:
            async with session.begin():          # avtomatik commit yoki rollback
                data["session"] = session
                return await handler(event, data)
```

Handler'da session parametr sifatida keladi:

```python
@router.message(Command("start"))
async def start(message: Message, session: AsyncSession) -> None:
    user = await crud.get_user(message.from_user.id, session)
```

---

## Migratsiyalar (Alembic)

### Nima uchun kerak?

Model o'zgarganda (yangi ustun, yangi jadval) mavjud DB ni buzmasdan yangilash uchun.

### Birinchi marta sozlash

```bash
# Alembic ni ishga tushirish (bir marta)
uv run alembic init alembic

# alembic/env.py ga modellarni ulash
# target_metadata = Base.metadata
```

### Ishlatish

```bash
# Yangi migration yaratish (model o'zgarishlarini aniqlaydi)
uv run alembic revision --autogenerate -m "add users table"

# Migratsiyani qo'llash
uv run alembic upgrade head

# Bir qadam orqaga
uv run alembic downgrade -1

# Joriy holat
uv run alembic current

# Barcha migratsiyalar tarixi
uv run alembic history
```

---

## SQLite vs PostgreSQL

| | SQLite | PostgreSQL |
|---|---|---|
| O'rnatish | O'rnatish shart emas | Server kerak |
| Local ishlatish | ✅ Ideal | ❌ Qo'shimcha sozlash |
| Production | ⚠️ Kichik loyihalar uchun | ✅ Tavsiya etiladi |
| Concurrent so'rovlar | ❌ Cheklangan | ✅ Yaxshi |

**Switching (SQLite → PostgreSQL):**

`.env` da faqat `DATABASE_URL` ni o'zgartiring:

```env
# SQLite dan
DATABASE_URL=sqlite+aiosqlite:///data/bot.db

# PostgreSQL ga
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/botdb
```

`pyproject.toml` ga `asyncpg` qo'shing:

```bash
uv add asyncpg
```

Keyin migratsiyalarni qayta qo'llang:

```bash
uv run alembic upgrade head
```
