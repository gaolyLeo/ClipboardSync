import io
import os
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import asyncio
import logging
from clipboard_manager import ClipboardManager

logger = logging.getLogger(__name__)

class TelegramHandler:
    """Telegram message handler"""
    
    def __init__(self, client: TelegramClient):
        self.client = client
        self.clipboard = ClipboardManager()
        self._register_handlers()

    def _register_handlers(self):
        """Register message event handlers"""
        self.client.add_event_handler(self.message_handler, events.NewMessage(outgoing=False))

    async def message_handler(self, event: events.NewMessage.Event):
        """Unified message processing entry point"""
        try:
            text = event.raw_text.lower()
            if text.startswith('/push'):
                await self.process_push(event)
            elif text.startswith('/pull'):
                await self.process_pull(event)
            elif text == '/stop':
                await self.process_stop()
        except Exception as e:
            logger.exception("Message processing error")
            await event.reply("Error processing request")

    async def process_push(self, event):
        """Handle /push command"""
        if event.message.media:
            await self._process_media(event)
        else:
            text = event.raw_text.replace('/push', '', 1).strip()
            if text:
                if self.clipboard.set_text(text):
                    await event.reply("✅ Text copied")
                else:
                    await event.reply("❌ Text copy failed")

    async def _process_media(self, event):
        """Handle media messages"""
        if isinstance(event.message.media, (MessageMediaPhoto, MessageMediaDocument)):
            image_bytes = await self._download_media(event)
            if image_bytes and self.clipboard.set_image(image_bytes):
                await event.reply("✅ Image copied")
            else:
                await event.reply("❌ Image copy failed")

    async def _download_media(self, event) -> io.BytesIO:
        """Download media file to memory"""
        image_bytes = io.BytesIO()
        await event.client.download_media(event.message, file=image_bytes)
        image_bytes.seek(0)
        return image_bytes

    async def process_pull(self, event):
        """Handle /pull command"""
        if self.clipboard.has_image():
            await self._send_image(event)
        else:
            await self._send_text(event)

    async def _send_image(self, event):
        """Send clipboard image"""
        if image_path := self.clipboard.get_image():
            try:
                await event.reply(file=image_path)
            except Exception as e:
                await event.reply("❌ Failed to send image")
            finally:
                os.unlink(image_path)

    async def _send_text(self, event):
        """Send clipboard text"""
        if text := self.clipboard.get_text():
            await event.reply(text[:4096])
        else:
            await event.reply("📭 Clipboard is empty")

    async def process_stop(self):
        """Handle /stop command"""
        logger.info("Received stop command")
        await self.client.disconnect()