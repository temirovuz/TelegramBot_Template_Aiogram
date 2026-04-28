# Deployment qo'llanmasi

## Muhitlar

| Muhit | Tavsif |
|---|---|
| `local` | Ishlab chiqish — polling rejimi |
| `production` | Server — polling yoki webhook |

---

## Local (ishlab chiqish)

```bash
# Bog'liqliklarni o'rnating
uv sync

# .env sozlang
cp .env.example .env

# DB migratsiyalarini qo'llang
uv run alembic upgrade head

# Botni ishga tushiring
uv run python main.py
```

---

## Production — VPS (Linux)

### Talab qilinadigan narsa
- Ubuntu 22.04+ yoki Debian 12+
- Python 3.12+
- Kamida 512MB RAM

### 1. Serverni tayyorlash

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl
```

### 2. uv o'rnatish

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 3. Loyihani klonlash

```bash
git clone https://github.com/username/my-bot.git
cd my-bot
uv sync --no-dev
```

### 4. .env sozlash

```bash
cp .env.example .env
nano .env
```

```env
BOT_TOKEN=your_real_token
DATABASE_URL=sqlite+aiosqlite:///data/bot.db
ADMIN_IDS=123456789
LOG_LEVEL=INFO
```

### 5. DB migratsiyalari

```bash
mkdir -p data
uv run alembic upgrade head
```

### 6. Systemd service yaratish

```bash
sudo nano /etc/systemd/system/mybot.service
```

```ini
[Unit]
Description=My Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/my-bot
ExecStart=/home/ubuntu/.local/bin/uv run python main.py
Restart=always
RestartSec=10
EnvironmentFile=/home/ubuntu/my-bot/.env
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mybot
sudo systemctl start mybot

# Holatini tekshirish
sudo systemctl status mybot

# Loglarni ko'rish
sudo journalctl -u mybot -f
```

---

## Production — Docker

### Dockerfile (loyiha ildizida mavjud bo'lishi kerak)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN uv run alembic upgrade head

CMD ["uv", "run", "python", "main.py"]
```

### docker-compose.yml

```yaml
services:
  bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data
```

### Ishga tushirish

```bash
# Build va ishga tushirish
docker compose up -d --build

# Loglarni ko'rish
docker compose logs -f bot

# To'xtatish
docker compose down
```

---

## Yangilash (update)

### VPS (systemd)

```bash
cd /home/ubuntu/my-bot
git pull origin main
uv sync --no-dev
uv run alembic upgrade head
sudo systemctl restart mybot
```

### Docker

```bash
git pull origin main
docker compose up -d --build
```

---

## Monitoring va loglar

### Loglarni ko'rish

```bash
# Systemd
sudo journalctl -u mybot -n 100 --no-pager

# Docker
docker compose logs -f --tail=100 bot
```

### Bot ishlayaptimi tekshirish

```bash
# Systemd
sudo systemctl is-active mybot

# Docker
docker compose ps
```

---

## Muhim xavfsizlik qoidalari

1. `.env` faylini hech qachon git'ga push qilmang
2. Bot token'ini hech kim bilan ulashmang
3. `ADMIN_IDS` ni faqat ishonchli kishilar bilan to'ldiring
4. Serverni muntazam yangilang: `sudo apt upgrade -y`
5. Firewall'ni yoqing: `sudo ufw allow ssh && sudo ufw enable`
