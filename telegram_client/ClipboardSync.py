import logging
import os
import io
import tempfile
from PIL import Image
from typing import Union
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import asyncio
import win32clipboard
import win32con

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

API_ID = int(os.getenv('TG_API_ID', '22723964'))
API_HASH = os.getenv('TG_API_HASH', '9cf771f2f485dac778e058b9800b2d9b')
PHONE = os.getenv('TG_PHONE', '+85294931574')

# Initialize client
client = TelegramClient(
    session='user_session',
    api_id=API_ID,
    api_hash=API_HASH,
    connection_retries=100,
    auto_reconnect=True,
    timeout=60
)

class ClipboardManager:
    """
    A utility class for managing clipboard operations, including copying and retrieving text and images.
    Supports integration with Telegram for cross-device clipboard sharing.
    """
    def set_text(self, text: str) -> bool:
        """Copies text to the system clipboard."""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            logger.info("Copied %d characters to clipboard", len(text))
            return True
        except Exception as e:
            logger.error("Failed to copy text to clipboard: %s", str(e))
            return False

    def set_image(self, image_bytes: io.BytesIO) -> bool:
        """
        Copies an image to the system clipboard.
        Args:
            image_bytes (io.BytesIO): Image data in BytesIO format.
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            img = Image.open(image_bytes)
            output = io.BytesIO()
            img.save(output, 'BMP')
            data = output.getvalue()[14:]  # Skip BMP header for DIB format
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logger.info("Copied image to clipboard")
            return True
        except Exception as e:
            logger.error("Failed to copy image to clipboard: %s", str(e))
            return False

    def get_text(self) -> str:
        """Retrieves text from the system clipboard."""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return text or ""
            win32clipboard.CloseClipboard()
            return ""
        except Exception as e:
            logger.error("Failed to get text from clipboard: %s", str(e))
            return ""

    def get_clipboard_image(self) -> Union[str, None]:
        """
        Retrieves an image from the clipboard and saves it as a temporary PNG file.
        Returns:
            str or None: Path to the temporary file, or None if no image is available.
        """
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                image = Image.open(io.BytesIO(data))  # Convert DIB to PIL Image
                temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                image.save(temp_file, format="PNG")  # Save as PNG for Telegram compatibility
                temp_file.close()
                win32clipboard.CloseClipboard()
                return temp_file.name
            win32clipboard.CloseClipboard()
            return None
        except Exception as e:
            logger.error("Error extracting clipboard image: %s", str(e))
            return None

    def has_image(self) -> bool:
        """Checks if the clipboard contains an image."""
        try:
            win32clipboard.OpenClipboard()
            has_image = win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB)
            win32clipboard.CloseClipboard()
            return has_image
        except Exception as e:
            logger.error("Error checking clipboard for image: %s", str(e))
            return False
async def download_image(event):
    image_bytes = io.BytesIO()
    await event.client.download_media(event.message, file=image_bytes)
    image_bytes.seek(0)
    return image_bytes

async def process_push(event):
    clipboard = ClipboardManager()
    if event.message.media:
        if isinstance(event.message.media, MessageMediaPhoto) or \
           (isinstance(event.message.media, MessageMediaDocument) and 
            event.message.media.document.mime_type.startswith('image/')):
            image_bytes = await download_image(event)
            if clipboard.set_image(image_bytes):
                await event.reply("Image copied to clipboard")
            else:
                await event.reply("Failed to copy image to clipboard")
        else:
            await event.reply("Unsupported media type")
    else:
        text = event.raw_text
        if text.startswith('/push'):
            text = text.replace('/push', '', 1).strip()
        if text:
            if clipboard.set_text(text):
                await event.reply("Text copied to clipboard")
            else:
                await event.reply("Failed to copy text to clipboard")
        else:
            await event.reply("No text to copy")

async def process_pull(event, sender):
    clipboard = ClipboardManager()
    if clipboard.has_image():
        image_path = clipboard.get_clipboard_image()
        if image_path:
            try:
                await client.send_file(
                    entity=sender,
                    file=image_path,
                    caption="Image from clipboard"
                )
                logger.info("Sent image from clipboard")
            except Exception as e:
                logger.error(f"Error sending image: {e}")
                await event.reply("Failed to send image")
            finally:
                # Clean up temporary file
                try:
                    os.unlink(image_path)
                except Exception as e:
                    logger.error(f"Error deleting temporary file: {e}")
    else:
        content = clipboard.get_text()
        if content:
            if len(content) > 4096:
                await event.reply("Content too long, truncated to 4096 characters")
                content = content[:4096]
            await client.send_message(
                entity=sender,
                message=content,
                link_preview=False
            )
            logger.info("Sent %d characters from clipboard", len(content))
        else:
            await event.reply("Clipboard is empty")

@client.on(events.NewMessage(outgoing=False))
async def message_handler(event):
    try:
        sender = await event.get_sender()

        text = event.raw_text.lower()
        if text.startswith('/push'):
            await process_push(event)
        elif text.startswith('/pull'):
            await process_pull(event, sender)
        elif text == '/stop':
            logger.info("Received /stop command, shutting down...")
            await client.disconnect()
    except Exception as e:
        logger.exception("Error processing message: %s", str(e))
        await event.reply("Error processing your request")

async def main():
    try:
        await client.start(
            phone=lambda: PHONE,
            max_attempts=3,
            code_callback=lambda: input("Enter 2FA code: ") if client.is_connected() else None
        )
        logger.info("Successfully logged in as: %s (ID: %s)", 
                    (await client.get_me()).first_name, (await client.get_me()).id)
        
        await client.run_until_disconnected()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        logger.info("Received interrupt, shutting down...")
        await client.disconnect()
    finally:
        logger.info("Client disconnected")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error("Program terminated unexpectedly: %s", str(e))
    finally:
        logger.info("Program exited")