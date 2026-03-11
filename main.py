import asyncio
import logging
import asyncpg
from telethon import TelegramClient, events
from datetime import datetime
from decouple import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')
SESSION_NAME = config('SESSION_NAME', default='session')
TIMEOUT = config('TIMEOUT', default=60, cast=int)

DB_CONFIG = {
    'user': config('DB_USER', default='postgres'),
    'password': config('DB_PASSWORD'),
    'database': config('DB_NAME', default='postgres'),
    'host': config('DB_HOST', default='localhost'),
    'port': config('DB_PORT', default=5432, cast=int),
}


async def db_connect() -> asyncpg.Connection:
    conn = await asyncpg.connect(**DB_CONFIG)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id          SERIAL PRIMARY KEY,
            user_id     BIGINT,
            channel_id  BIGINT,
            message_id  BIGINT,
            channel_username TEXT,
            message     TEXT,
            timestamp   BIGINT
        );
    ''')
    logger.info("Connected to PostgreSQL")
    return conn


async def db_insert(conn: asyncpg.Connection, user_id: int, channel_id: int,
                    message_id: int, channel_username: str, message: str) -> None:
    timestamp = int(datetime.now().timestamp())
    await conn.execute(
        '''INSERT INTO messages
               (user_id, channel_id, message_id, channel_username, message, timestamp)
           VALUES ($1, $2, $3, $4, $5, $6);''',
        user_id, channel_id, message_id, channel_username, message, timestamp
    )


async def main() -> None:
    conn = await db_connect()

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH, timeout=TIMEOUT)

    @client.on(events.NewMessage)
    async def handle_message(event: events.NewMessage.Event) -> None:
        user_id = getattr(event.from_id, 'user_id', None)
        if user_id is None:
            return  # skip channel/anonymous posts

        channel_id = event.chat_id
        message_id = event.id
        message = event.message.message or ''

        try:
            peer = await client.get_input_entity(event.peer_id)
            entity = await client.get_entity(peer)
            channel_username = getattr(entity, 'username', None) or getattr(entity, 'title', 'unknown')
        except Exception as exc:
            channel_username = 'unknown'
            logger.warning("Could not resolve channel info: %s", exc)

        logger.info(
            "user=%s  channel=%s (@%s)  msg_id=%s  text=%.50r",
            user_id, channel_id, channel_username, message_id, message
        )

        try:
            await db_insert(conn, user_id, channel_id, message_id, channel_username, message)
        except Exception as exc:
            logger.error("DB insert failed: %s", exc)

    async with client:
        await client.start()
        logger.info("Telegram client started. Listening for new messages...")
        try:
            await client.run_until_disconnected()
        finally:
            await conn.close()
            logger.info("Database connection closed")


if __name__ == '__main__':
    asyncio.run(main())
