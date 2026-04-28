# Handler'lar hujjati

## Handler nima?

Handler — Telegram'dan kelgan xabar, buyruq yoki callback'ni qabul qilib, javob qaytaruvchi asinxron funksiya.

---

## Tuzilishi

```
handlers/
├── __init__.py          # main_router, barcha router'larni birlashtiradi
├── common/
│   ├── __init__.py
│   ├── start.py         # /start — hamma uchun
│   └── help.py          # /help — hamma uchun
├── user/
│   ├── __init__.py
│   ├── profile.py       # profil ko'rish, tahrirlash
│   └── settings.py      # foydalanuvchi sozlamalari
└── admin/
    ├── __init__.py
    └── users.py          # foydalanuvchilarni boshqarish
```

---

## Handler yozish qoidalari

### Asosiy shablon

```python
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters.is_admin import IsAdmin
from services import user_service

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, session: AsyncSession) -> None:
    user = await user_service.get_or_create(message.from_user, session)
    await message.answer(f"Salom, {user.full_name}!")
```

### Callback handler

```python
from aiogram.types import CallbackQuery
from keyboards.user.inline import ProfileCallback

@router.callback_query(ProfileCallback.filter(F.action == "edit"))
async def edit_profile_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text("Ismingizni kiriting:")
```

### FSM bilan handler

```python
from aiogram.fsm.context import FSMContext
from states.register import RegisterStates

@router.message(Command("register"))
async def start_register(message: Message, state: FSMContext) -> None:
    await state.set_state(RegisterStates.waiting_for_name)
    await message.answer("Ismingizni kiriting:")


@router.message(RegisterStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(RegisterStates.waiting_for_phone)
    await message.answer("Telefon raqamingizni kiriting:")
```

---

## Mavjud handler'lar

### `/start` — `handlers/common/start.py`

**Trigger:** `/start` buyrug'i  
**Kimga:** Hamma foydalanuvchilarga  
**Nima qiladi:**
- Foydalanuvchini DB da topadi yoki yangi yaratadi
- Salomlashish xabari yuboradi
- Asosiy menyu tugmalarini ko'rsatadi

---

### `/help` — `handlers/common/help.py`

**Trigger:** `/help` buyrug'i  
**Kimga:** Hamma foydalanuvchilarga  
**Nima qiladi:**
- Mavjud buyruqlar ro'yxatini ko'rsatadi
- Yordam ma'lumotlarini beradi

---

### Profil — `handlers/user/profile.py`

**Trigger:** "Profilim" tugmasi yoki `/profile`  
**Kimga:** Ro'yxatdan o'tgan foydalanuvchilar  
**Nima qiladi:**
- Foydalanuvchi ma'lumotlarini ko'rsatadi
- Tahrirlash imkoniyatini beradi

---

### Sozlamalar — `handlers/user/settings.py`

**Trigger:** "Sozlamalar" tugmasi  
**Kimga:** Ro'yxatdan o'tgan foydalanuvchilar  
**Nima qiladi:**
- Til tanlash
- Bildirishnomalarni yoqish/o'chirish

---

### Foydalanuvchilar — `handlers/admin/users.py`

**Trigger:** `/users` buyrug'i  
**Kimga:** Faqat adminlar (`IsAdmin` filteri)  
**Nima qiladi:**
- Foydalanuvchilar ro'yxatini ko'rsatadi
- Bloklash/blokdan chiqarish
- Statistika

---

## Yangi handler qo'shish

### 1. Fayl yarating

```bash
touch handlers/user/payment.py
```

### 2. Router va handler yozing

```python
# handlers/user/payment.py
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(F.text == "To'lov")
async def payment_menu(message: Message) -> None:
    await message.answer("To'lov bo'limi")
```

### 3. `handlers/__init__.py` ga ulang

```python
from handlers.user.payment import router as payment_router

main_router.include_router(payment_router)
```

Shu bilan handler ishlaydi — `main.py` ga tegish shart emas.

---

## Xatolarni ushlash

Barcha handler'larda yuzaga kelgan kutilmagan xatolar `errors.py` da markaziy ushlashadi:

```python
# handlers/errors.py — bo'lishi tavsiya etiladi
from aiogram.types import ErrorEvent

@router.errors()
async def error_handler(event: ErrorEvent) -> None:
    logger.error("Handler xatosi", exc_info=event.exception)
    # foydalanuvchiga xato xabari yuborish
```
