# Arxitektura hujjati

## Umumiy ko'rinish

Loyiha **qatlamli arxitektura** (Layered Architecture) tamoyilida qurilgan. Har bir qatlam faqat o'zidan pastdagi qatlam bilan gaplashadi — bu kodni test qilishni, kengaytirishni va tushunishni osonlashtiradi.

```
┌─────────────────────────────────┐
│         handlers/               │  ← Telegram so'rovlarini qabul qiladi
│  (Presentation layer)           │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         services/               │  ← Biznes mantiqni bajaradi
│  (Application layer)            │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│           db/crud.py            │  ← DB operatsiyalari
│  (Data Access layer)            │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│          db/models.py           │  ← Jadval ta'riflari
│  (Infrastructure layer)         │
└─────────────────────────────────┘
```

---

## Qatlamlar va ularning mas'uliyati

### 1. Handlers (`handlers/`)

**Nima qiladi:** Telegram'dan kelgan xabar va callback'larni qabul qiladi, javob qaytaradi.

**Qoidalar:**
- Handler faqat Telegram logikasini biladi: `message`, `callback_query`, `FSMContext`
- Biznes mantiq **yo'q** — faqat `service` funksiyasini chaqirish
- Validatsiya **yo'q** — filter yoki middleware qiladi
- To'g'ridan-to'g'ri DB **yo'q** — faqat `crud` orqali

```python
# To'g'ri
@router.message(F.text == "Profilim")
async def show_profile(message: Message, session: AsyncSession):
    user = await user_service.get_profile(message.from_user.id, session)
    await message.answer(format_profile(user))

# Noto'g'ri — handler ichida biznes mantiq va to'g'ridan-to'g'ri DB
@router.message(F.text == "Profilim")
async def show_profile(message: Message, session: AsyncSession):
    user = await session.execute(select(User).where(...))  # ❌
    if user.is_banned:                                      # ❌ biznes mantiq
        ...
```

**Tuzilishi:**
```
handlers/
├── common/     # Hamma uchun: /start, /help
├── user/       # Oddiy foydalanuvchilar uchun
└── admin/      # Faqat adminlar uchun
```

---

### 2. Services (`services/`)

**Nima qiladi:** Biznes qoidalarni bajaradi. "Agar foydalanuvchi bloklangan bo'lsa nima bo'ladi?" — bu savol services'da javobini topadi.

**Qoidalar:**
- Aiogram ob'ektlarini bilmaydi (`Message`, `CallbackQuery` yo'q)
- `crud` funksiyalarini chaqiradi, lekin o'zi SQL yozmaydi
- Bir necha `crud` chaqiruvini birlashtirib murakkab amal qilishi mumkin
- Exception'larni o'zi ko'taradi yoki handle qiladi

```python
# services/user_service.py
async def register_user(telegram_id: int, username: str, session: AsyncSession) -> User:
    existing = await crud.get_user(telegram_id, session)
    if existing:
        raise UserAlreadyExistsError(telegram_id)

    user = await crud.create_user(telegram_id, username, session)
    await notification_service.send_welcome(user)
    return user
```

---

### 3. DB / CRUD (`db/`)

**`models.py`** — SQLAlchemy ORM jadval ta'riflari. Faqat jadval strukturasi, biznes mantiq yo'q.

**`crud.py`** — Create, Read, Update, Delete operatsiyalari. Faqat SQL/ORM so'rovlari, biznes qoidalar yo'q.

```python
# db/crud.py
async def get_user(telegram_id: int, session: AsyncSession) -> User | None:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()
```

---

### 4. Core (`core/`)

**`config.py`** — `.env` faylidan sozlamalarni o'qiydi. Butun loyihada bitta `settings` obyekti ishlatiladi.

**`logger.py`** — Loguru yoki structlog sozlamalari. Har bir modul shu logger'dan foydalanadi.

---

### 5. Filters (`filters/`)

Handler'ga so'rov yetib kelishidan **oldin** shartni tekshiradi.

```python
# filters/is_admin.py
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.ADMIN_IDS
```

Handler'da:
```python
@router.message(IsAdmin(), Command("ban"))
async def ban_user(message: Message): ...
```

---

### 6. Middlewares (`middlewares/`)

Har bir so'rovdan oldin va keyin ishlaydigan qatlam. Filterdan farqi — middleware **hamma** so'rovga tegishli.

Odatdagi middleware'lar:
- `db_session` — har so'rov uchun DB sessiyasini ochib, handler'ga uzatadi
- `throttling` — bir foydalanuvchidan juda tez kelgan so'rovlarni to'xtatadi
- `auth` — foydalanuvchini DB'da topadi yoki yaratadi

---

### 7. States (`states/`)

FSM (Finite State Machine) — ko'p bosqichli dialog uchun. Masalan, ro'yxatdan o'tish:

```
START → ISM_KIRITING → TELEFON_KIRITING → TASDIQLASH → TUGADI
```

```python
# states/register.py
class RegisterStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_confirm = State()
```

---

## Ma'lumotlar oqimi (Data Flow)

```
Foydalanuvchi xabar yuboradi
         │
         ▼
    Middleware
    (session ochish, throttle tekshirish, userni topish)
         │
         ▼
      Filter
    (admin? obunachimi? holat to'g'rimi?)
         │
         ▼
     Handler
    (so'rovni qabul qilish, service'ni chaqirish)
         │
         ▼
     Service
    (biznes mantiq bajarish)
         │
         ▼
      CRUD
    (DB ga yozish/o'qish)
         │
         ▼
     Handler
    (javob formatlash va yuborish)
         │
         ▼
Foydalanuvchi javob oladi
```

---

## Router'larni ulash tartibi

`handlers/__init__.py` da barcha router'lar `main_router`ga ulanadi:

```python
from aiogram import Router
from handlers.common.start import router as start_router
from handlers.common.help import router as help_router
from handlers.user.profile import router as profile_router
from handlers.user.settings import router as settings_router
from handlers.admin.users import router as admin_users_router

main_router = Router()
main_router.include_routers(
    start_router,
    help_router,
    profile_router,
    settings_router,
    admin_users_router,
)
```

`main.py` da faqat `main_router` ulanadi:
```python
dp.include_router(main_router)
```

---

## Kengaytirish bo'yicha tavsiyalar

| Ehtiyoj | Yechim |
|---|---|
| To'lov tizimi | `handlers/user/payment.py` + `services/payment_service.py` |
| Xabarnomalar yuborish | `services/notification_service.py` + Celery/arq |
| Ko'p til (i18n) | `locales/` + `fluent` yoki `babel` |
| Keshlaш | `Redis` + `core/cache.py` |
| Admin statistika | `handlers/admin/stats.py` + SQLAlchemy aggregate so'rovlar |
| Webhook | `main.py` da polling o'rniga aiohttp/fastapi |
