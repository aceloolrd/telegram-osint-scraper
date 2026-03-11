# Telegram OSINT Scraper

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telethon](https://img.shields.io/badge/Telethon-1.36-green)](https://github.com/LonamiWebs/Telethon)

A Telegram userbot that listens to incoming messages across all chats and channels the account is subscribed to, and stores structured data in a PostgreSQL database for further analysis.

> **Intended use:** research, monitoring of public channels with the account owner's consent, and educational purposes.

---

## Features

- Real-time message capture via [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto)
- Stores `user_id`, `channel_id`, `message_id`, `channel_username`, message text and Unix timestamp
- Async I/O throughout — `asyncio` + `asyncpg`
- Graceful shutdown with proper DB connection cleanup
- All credentials via environment variables (`.env`)
- Structured logging with timestamps

## Tech Stack

| Layer | Technology |
|---|---|
| Telegram API | Telethon 1.36 |
| Database | PostgreSQL + asyncpg |
| Config | python-decouple |
| Runtime | Python 3.10+, asyncio |

---

## Project Structure

```
telegram-osint-scraper/
├── main.py            # Entry point — client + event handler
├── requirements.txt   # Dependencies
├── .env.example       # Environment variables template
└── .gitignore
```

---

## Quick Start

### 1. Get Telegram API credentials

Go to [my.telegram.org/apps](https://my.telegram.org/apps), create an app and copy `API_ID` and `API_HASH`.

### 2. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/telegram-osint-scraper.git
cd telegram-osint-scraper
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env — fill in API_ID, API_HASH, DB_PASSWORD
```

### 4. Set up PostgreSQL

```sql
CREATE DATABASE osint;
```

Update `DB_NAME` in `.env` accordingly.

### 5. Run

```bash
python main.py
```

On first run Telethon will ask for your phone number and a confirmation code to create a session file.

---

## Database Schema

```sql
CREATE TABLE messages (
    id               SERIAL PRIMARY KEY,
    user_id          BIGINT,
    channel_id       BIGINT,
    message_id       BIGINT,
    channel_username TEXT,
    message          TEXT,
    timestamp        BIGINT   -- Unix timestamp
);
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_ID` | yes | — | Telegram app API ID |
| `API_HASH` | yes | — | Telegram app API hash |
| `SESSION_NAME` | no | `session` | Name for the `.session` file |
| `TIMEOUT` | no | `60` | MTProto request timeout (seconds) |
| `DB_USER` | no | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | yes | — | PostgreSQL password |
| `DB_NAME` | no | `postgres` | Database name |
| `DB_HOST` | no | `localhost` | Database host |
| `DB_PORT` | no | `5432` | Database port |

---

---

# Telegram OSINT Scraper — RU

Userbot на Telethon, который в реальном времени перехватывает входящие сообщения из всех чатов и каналов, на которые подписан аккаунт, и сохраняет структурированные данные в PostgreSQL.

> **Назначение:** исследование, мониторинг публичных каналов с согласия владельца аккаунта, образовательные цели.

## Возможности

- Захват сообщений в реальном времени через [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto)
- Сохранение `user_id`, `channel_id`, `message_id`, имени канала, текста и Unix-метки времени
- Полностью асинхронный стек — `asyncio` + `asyncpg`
- Корректное завершение работы (graceful shutdown) с закрытием соединения
- Все credentials через переменные окружения (`.env`)
- Структурированное логирование с временными метками

## Быстрый старт

### 1. Получить API-ключи Telegram

Зайди на [my.telegram.org/apps](https://my.telegram.org/apps), создай приложение, скопируй `API_ID` и `API_HASH`.

### 2. Клонировать и установить зависимости

```bash
git clone https://github.com/YOUR_USERNAME/telegram-osint-scraper.git
cd telegram-osint-scraper
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Настроить окружение

```bash
cp .env.example .env
# Заполни API_ID, API_HASH, DB_PASSWORD в .env
```

### 4. Создать БД

```sql
CREATE DATABASE osint;
```

Обнови `DB_NAME` в `.env`.

### 5. Запуск

```bash
python main.py
```

При первом запуске Telethon запросит номер телефона и код подтверждения для создания сессионного файла.
