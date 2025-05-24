from typing import Union
import win32clipboard
import win32con
from PIL import Image
import io
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

class ClipboardManager:
    """Core class for system clipboard management"""
    
    def __init__(self):
        self.lock = True  # Lock for thread safety

    def set_text(self, text: str) -> bool:
        """Safely set clipboard text"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            logger.info("Copied %d characters to clipboard", len(text))
            return True
        except Exception as e:
            logger.error("Text copy failed: %s", str(e))
            return False
        finally:
            win32clipboard.CloseClipboard()

    def set_image(self, image_bytes: io.BytesIO) -> bool:
        """Convert and set clipboard image"""
        try:
            img = Image.open(image_bytes)
            with io.BytesIO() as output:
                img.save(output, 'BMP')
                data = output.getvalue()[14:]
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_DIB, data)
                logger.info("Image copied to clipboard")
                return True
        except Exception as e:
            logger.error("Image copy failed: %s", str(e))
            return False
        finally:
            win32clipboard.CloseClipboard()

    def get_text(self) -> str:
        """Safely get clipboard text"""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT) or ""
            return ""
        except Exception as e:
            logger.error("Get text failed: %s", str(e))
            return ""
        finally:
            win32clipboard.CloseClipboard()

    def get_image(self) -> Union[str, None]:
        """Get clipboard image and return temporary file path"""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                Image.open(io.BytesIO(data)).save(temp_file, "PNG")
                temp_file.close()
                win32clipboard.CloseClipboard()
                return temp_file.name
            else:
                win32clipboard.CloseClipboard()
                return None
        except Exception as e:
            logger.error("Get image failed: %s", str(e))
            return None

    def has_image(self) -> bool:
        """Check if clipboard has image"""
        try:
            win32clipboard.OpenClipboard()
            return win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB)
        except Exception as e:
            logger.error("Check image failed: %s", str(e))
            return False
        finally:
            win32clipboard.CloseClipboard()