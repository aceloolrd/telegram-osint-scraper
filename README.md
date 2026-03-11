# Telegram OSINT Scraper

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telethon](https://img.shields.io/badge/Telethon-1.36-green)](https://github.com/LonamiWebs/Telethon)

A Telegram userbot that listens to incoming messages across all chats and channels the account is subscribed to, and stores structured data in a PostgreSQL database for further analysis.

> **Intended use:** research, monitoring of public channels with the account owner's consent, and educational purposes.

---

## ⚠️ Account Safety — Will Telegram Ban You?

**Short answer:** Telegram does not ban accounts for using Telethon itself. It bans accounts for *suspicious behavior patterns* — and Telethon is frequently used by spammers, so Telegram's spam detection is quite aggressive toward userbots.

### What actually triggers bans

| Trigger | Risk level |
|---|---|
| Rapid fire requests with no delays | High |
| Fresh account (< few days old) | High |
| VoIP / virtual phone number | High |
| Mass messaging or advertising | High |
| Suspicious IP / datacenter host | Medium |
| Reading messages without interaction | Low |
| Monitoring channels you're already in | Low |

### Telegram's Terms of Service

The [Telegram API ToS](https://core.telegram.org/api/terms) explicitly forbids:
- Performing actions on behalf of a user **without their knowledge and consent**
- Interfering with read receipts, online status, or self-destruct timers
- Using collected data to train ML/AI models

Violators get a **10-day warning**, then API access is revoked. Permanent account suspension is possible for severe violations (spam, phishing).

### Error codes you may encounter

| Code | Meaning |
|---|---|
| `401 USER_DEACTIVATED_BAN` | Account suspended |
| `420 FLOOD_WAIT_X` | Rate limit hit — wait X seconds |
| `PeerFloodError` | Account temporarily limited on certain peers |

### Best practices to stay safe

- **Use an established account** — don't run this on a freshly created one
- **Real SIM, not VoIP** — virtual numbers are high-risk
- **Respect rate limits** — Telegram's undocumented soft limit is ~1 req/sec per chat
- **Handle `FloodWaitError`** — Telethon does this automatically, don't override it
- **Check account status** — message [@SpamBot](https://t.me/spambot) inside Telegram to see if you're flagged
- **Only monitor chats you're subscribed to** — don't mass-join channels just to scrape

If you get banned: contact `abuse@telegram.org` or use [telegram.org/support](https://telegram.org/support).

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

## ⚠️ Безопасность аккаунта — банит ли Telegram за Telethon?

**Коротко:** Telegram не банит за использование Telethon как такового. Он банит за **подозрительные паттерны поведения** — но так как Telethon активно используется спамерами, антиспам-системы Telegram очень агрессивны по отношению к юзерботам.

### Что реально вызывает бан

| Триггер | Риск |
|---|---|
| Много запросов без задержек | Высокий |
| Свежий аккаунт (< нескольких дней) | Высокий |
| VoIP / виртуальный номер | Высокий |
| Массовая рассылка или реклама | Высокий |
| Подозрительный IP / хостинг ДЦ | Средний |
| Чтение сообщений без активных действий | Низкий |
| Мониторинг каналов, на которые уже подписан | Низкий |

### Правила использования API Telegram

[ToS Telegram API](https://core.telegram.org/api/terms) явно запрещает:
- Выполнять действия от имени пользователя **без его ведома и согласия**
- Вмешиваться в статус прочтения, онлайн-статус, самоуничтожение сообщений
- Использовать собранные данные для обучения ML/AI-моделей

Нарушителям дают **10 дней** на исправление, затем доступ к API отзывается. За спам/фишинг — постоянная блокировка аккаунта.

### Коды ошибок

| Код | Значение |
|---|---|
| `401 USER_DEACTIVATED_BAN` | Аккаунт заблокирован |
| `420 FLOOD_WAIT_X` | Rate limit — нужно подождать X секунд |
| `PeerFloodError` | Аккаунт временно ограничен для части контактов |

### Как снизить риск

- **Используй устоявшийся аккаунт** — не запускай на только что созданном
- **Реальная SIM-карта, не VoIP** — виртуальные номера в зоне высокого риска
- **Соблюдай rate limits** — неофициальный мягкий лимит Telegram ~1 запрос/сек на чат
- **Не перехватывай `FloodWaitError`** — Telethon обрабатывает его автоматически
- **Проверь статус аккаунта** — напиши [@SpamBot](https://t.me/spambot) в Telegram, он покажет, помечен ли аккаунт
- **Мониторь только подписки** — не вступай в каналы массово ради сбора данных

Если заблокировали: `abuse@telegram.org` или [telegram.org/support](https://telegram.org/support).

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
