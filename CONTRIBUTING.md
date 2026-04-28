# Hissa qo'shish bo'yicha qo'llanma

Loyihaga hissa qo'shmoqchi bo'lganingiz uchun rahmat! Quyidagi qoidalarga amal qiling.

---

## Mundarija

- [Kodeks](#kodeks)
- [Muammo bildirish (Issue)](#muammo-bildirish)
- [Yangi funksiya taklif qilish](#yangi-funksiya-taklif-qilish)
- [Pull Request yuborish](#pull-request-yuborish)
- [Ishlab chiqish muhitini sozlash](#ishlab-chiqish-muhitini-sozlash)
- [Kod uslubi](#kod-uslubi)
- [Commit xabarlari](#commit-xabarlari)

---

## Kodeks

Bu loyihada hamma bir-biriga hurmat bilan munosabatda bo'lishi kutiladi. Kamsitiuvchi, haqoratli yoki diskriminatsion xatti-harakatlar qabul qilinmaydi.

---

## Muammo bildirish

Xato (bug) topgan bo'lsangiz:

1. Avval [mavjud issue'larni](../../issues) tekshiring — balki allaqachon bildirilgan
2. Yangi issue ochib quyidagilarni kiriting:
   - **Qisqa va aniq sarlavha**
   - **Xatoni qayta ishlab chiqarish qadamlari** (step-by-step)
   - **Kutilgan natija** va **haqiqiy natija**
   - **Muhit ma'lumotlari**: Python versiyasi, OS, aiogram versiyasi

**Namuna:**
```
Sarlavha: /start komandasi 500 xato qaytarmoqda

Qadam 1: Botni ishga tushirish
Qadam 2: /start yuborish
Kutilgan: "Salom!" xabari kelishi
Haqiqiy: "Internal Server Error" xatosi

Python: 3.12.3
aiogram: 3.10.0
OS: Ubuntu 22.04
```

---

## Yangi funksiya taklif qilish

1. Issue oching va `enhancement` yorlig'ini qo'ying
2. Quyidagilarni tushuntiring:
   - Funksiya nima muammoni hal qiladi?
   - Qanday ishlashi kerak?
   - Muqobil yechimlarni ko'rib chiqdingizmi?

Katta o'zgarishlar uchun avval issue'da muhokama qiling, keyin kod yozing — vaqtingizni tejaydi.

---

## Pull Request yuborish

1. Repozitoriyni fork qiling
2. Yangi branch yarating:
   ```bash
   git checkout -b feature/funksiya-nomi
   # yoki
   git checkout -b fix/xato-tavsifi
   ```
3. O'zgarishlar qiling va commit qiling (quyidagi uslubga amal qiling)
4. Push qiling:
   ```bash
   git push origin feature/funksiya-nomi
   ```
5. Pull Request oching va quyidagilarni kiriting:
   - Nima o'zgardi va nima uchun
   - Qaysi issue'ni yopadi (`Closes #123`)
   - Qanday test qildingiz

**PR qabul qilish shartlari:**
- [ ] Kod uslubiga mos
- [ ] Mavjud funksionallik buzilmagan
- [ ] Yangi handler/servis uchun asosiy test mavjud
- [ ] `docs/` yangilangan (agar kerak bo'lsa)

---

## Ishlab chiqish muhitini sozlash

```bash
# 1. Fork'ingizni klonlang
git clone https://github.com/YOUR_USERNAME/my-bot.git
cd my-bot

# 2. Upstream'ni ulang (asl repo)
git remote add upstream https://github.com/ORIGINAL_USERNAME/my-bot.git

# 3. Bog'liqliklarni o'rnating (dev bilan birga)
uv sync --dev

# 4. .env faylini sozlang
cp .env.example .env
# .env ni tahrirlang

# 5. Botni ishga tushirib tekshiring
uv run python main.py
```

### Upstream bilan sinxronlash

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## Kod uslubi

Bu loyihada `ruff` formatlash va linting uchun ishlatiladi.

```bash
# Tekshirish
uv run ruff check .

# Avtomatik tuzatish
uv run ruff check . --fix

# Formatlash
uv run ruff format .
```

**Asosiy qoidalar:**

- Funksiya va o'zgaruvchi nomlar: `snake_case`
- Klass nomlar: `PascalCase`
- Doimiylar: `UPPER_SNAKE_CASE`
- Har bir funksiya va klass uchun type hint majburiy
- Murakkab mantiq uchun docstring yozing

```python
# Yaxshi
async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    """ID bo'yicha foydalanuvchini qaytaradi, topilmasa None."""
    return await session.get(User, user_id)

# Yomon
async def getUser(id, s):
    return await s.get(User, id)
```

---

## Commit xabarlari

[Conventional Commits](https://www.conventionalcommits.org/) formatiga amal qiling:

```
<tur>(<qamrov>): <qisqa tavsif>

[ixtiyoriy tananing]

[ixtiyoriy izoh]
```

**Turlar:**

| Tur | Qachon ishlatiladi |
|---|---|
| `feat` | Yangi funksiya |
| `fix` | Xatoni tuzatish |
| `docs` | Faqat hujjatlar |
| `refactor` | Funksionallik o'zgarmagan qayta yozish |
| `test` | Test qo'shish yoki tuzatish |
| `chore` | Konfiguratsiya, bog'liqliklar |
| `perf` | Ishlash tezligini oshirish |

**Misollar:**

```bash
git commit -m "feat(handlers): admin uchun broadcast handler qo'shildi"
git commit -m "fix(db): duplicate user yaratilishini oldini olish"
git commit -m "docs(readme): o'rnatish qadamlari yangilandi"
git commit -m "refactor(services): user_service DI bilan qayta yozildi"
```

---

Savollaringiz bo'lsa, [Discussions](../../discussions) bo'limida so'rang.
