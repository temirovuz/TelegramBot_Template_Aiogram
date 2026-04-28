# 🤖 Telegram Bot

> Aiogram 3.x asosida qurilgan production-ready Telegram bot

---

## 📁 Loyiha strukturasi

```
.
├── core/
│   ├── config.py          # Sozlamalar (.env o'qish, pydantic-settings)
│   └── logger.py          # Loguru/structlog konfiguratsiyasi
│
├── db/
│   ├── models.py          # SQLAlchemy ORM modellari
│   └── crud.py            # Ma'lumotlar bazasi operatsiyalari
│
├── filters/
│   ├── is_admin.py        # Admin foydalanuvchilarni tekshirish
│   └── is_subscribed.py   # Kanalga obuna tekshiruvi
│
├── handlers/
│   ├── admin/
│   │   └── users.py       # Admin panel handler'lari
│   ├── common/
│   │   ├── start.py       # /start komandasi
│   │   └── help.py        # /help komandasi
│   └── user/
│       ├── profile.py     # Profil ko'rish va tahrirlash
│       └── settings.py    # Foydalanuvchi sozlamalari
│
├── keyboards/
│   ├── admin/
│   │   ├── inline.py      # Admin inline tugmalar
│   │   └── reply.py       # Admin reply tugmalar
│   └── user/
│       ├── inline.py      # Foydalanuvchi inline tugmalar
│       └── reply.py       # Foydalanuvchi reply tugmalar
│
├── middlewares/           # Oraliq qatlam (auth, throttling, ...)
├── services/              # Biznes logika
├── states/
│   └── register.py        # FSM ro'yxatdan o'tish holatlari
├── utils/                 # Yordamchi funksiyalar
│
├── main.py                # Kirish nuqtasi
├── pyproject.toml         # Loyiha bog'liqliklari (uv)
├── uv.lock                # Lock fayl
├── .env.example           # Muhit o'zgaruvchilari namunasi
├── .python-version        # Python versiyasi
└── .gitignore
```

---

## ⚙️ Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| [aiogram 3.x](https://docs.aiogram.dev/) | Telegram Bot framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM — ma'lumotlar bazasi |
| [Alembic](https://alembic.sqlalchemy.org/) | DB migratsiyalari |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Konfiguratsiya va validatsiya |
| [uv](https://docs.astral.sh/uv/) | Paket menejeri |

---

## 🚀 O'rnatish va ishga tushirish

### 1. Repozitoriyni klonlash

```bash
git clone https://github.com/username/my-bot.git
cd my-bot
```

### 2. Python versiyasini o'rnatish

```bash
# .python-version faylidagi versiya avtomatik tanlanadi
uv python install
```

### 3. Bog'liqliklarni o'rnatish

```bash
uv sync
```

### 4. Muhit o'zgaruvchilarini sozlash

```bash
cp .env.example .env
```

Keyin `.env` faylini oching va qiymatlarni to'ldiring:

```env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=sqlite+aiosqlite:///bot.db
ADMIN_IDS=123456789,987654321
```

### 5. Ma'lumotlar bazasini yaratish

```bash
uv run alembic upgrade head
```

### 6. Botni ishga tushirish

```bash
uv run python main.py
```

---

## 🛠️ Ishlab chiqish

### Virtual muhit

`uv` avtomatik `.venv` papkasini yaratadi. Qo'lda faollashtirish kerak bo'lsa:

```bash
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### Yangi handler qo'shish

1. `handlers/user/` yoki `handlers/admin/` ichiga yangi fayl yarating
2. Faylda `router = Router()` yarating va handler'larni qo'shing
3. `handlers/__init__.py` da router'ni `main_router`ga ulang:

```python
from handlers.user.yangi import router as yangi_router
main_router.include_router(yangi_router)
```

### Yangi migration yaratish

```bash
uv run alembic revision --autogenerate -m "add users table"
uv run alembic upgrade head
```

---

## 📐 Arxitektura

Loyiha **qatlamli arxitektura** (layered architecture) tamoyiliga asoslangan:

```
handlers/        ← Telegram so'rovlarini qabul qiladi
    ↓
services/        ← Biznes mantiqni bajaradi
    ↓
db/crud.py       ← Ma'lumotlar bazasi bilan ishlaydi
    ↓
db/models.py     ← Jadval ta'riflari
```

**Qoidalar:**
- Handler ichida faqat Telegram logikasi bo'lsin
- Biznes mantiq `services/` da bo'lsin
- `crud.py` faqat DB operatsiyalari qilsin — biznes qoidalar yo'q

---

## 🔐 .env o'zgaruvchilari

| O'zgaruvchi | Tavsif | Majburiy |
|---|---|---|
| `BOT_TOKEN` | BotFather'dan olingan token | ✅ |
| `DATABASE_URL` | SQLAlchemy ulanish string'i | ✅ |
| `ADMIN_IDS` | Admin foydalanuvchi ID'lari (vergul bilan) | ✅ |
| `LOG_LEVEL` | Loglash darajasi (`DEBUG`, `INFO`, ...) | ❌ |

---

## 🤝 Hissa qo'shish

1. Fork qiling
2. Yangi branch oching: `git checkout -b feature/yangi-funksiya`
3. O'zgarishlarni commit qiling: `git commit -m "feat: yangi funksiya qo'shildi"`
4. Push qiling: `git push origin feature/yangi-funksiya`
5. Pull Request oching

---

## 📄 Litsenziya

MIT License — batafsil [LICENSE](LICENSE) faylida.