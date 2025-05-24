import os
import asyncio
import logging
from telethon import TelegramClient
from telegram_handler import TelegramHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ClipboardSync:
    """Clipboard synchronization main program"""
    
    def __init__(self):
        self.client = self._init_client()
        self.handler = TelegramHandler(self.client)

    def _init_client(self) -> TelegramClient:
        """Initialize Telegram client"""
        return TelegramClient(
            session='user_session',
            api_id=int(os.getenv('TG_API_ID')),
            api_hash=os.getenv('TG_API_HASH'),
            connection_retries=100,
            auto_reconnect=True,
            timeout=60
        )

    async def start(self):
        """Start client"""
        try:
            await self.client.start(
                phone=lambda: os.getenv('TG_PHONE'),
                max_attempts=3
            )
            me = await self.client.get_me()
            logger.info(f"Logged in as {me.first_name} (ID: {me.id})")
            await self.client.run_until_disconnected()
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info("Graceful shutdown")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            await self.client.disconnect()

if __name__ == '__main__':
    # Load configuration from environment variables
    os.environ['TG_API_ID'] = 'YOUR_API_ID'
    os.environ['TG_API_HASH'] = 'YOUR_API_HASH'
    os.environ['TG_PHONE'] = 'YOUR_PHONE_NUMBER'
    app = ClipboardSync()
    asyncio.run(app.start())