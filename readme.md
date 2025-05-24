# 📋 ClipboardSync 

**Seamless Cross-Device Clipboard Sync via Telegram**

[![Telethon Version](https://img.shields.io/badge/telethon-1.25+-blue.svg)](https://docs.telethon.dev/)
[![Python Version](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Introduction
A robust clipboard synchronization system that bridges Windows and iOS devices using Telegram's encrypted messaging as the transport layer. Built with:

```python
# Core Technologies
from telethon import TelegramClient  # MTProto API wrapper
from PIL import Image  # Cross-platform image processing
import win32clipboard  # Windows clipboard integration
```

### 🚀 Key Features
| Feature                          | Implementation                              | Benefit                                      |
|----------------------------------|---------------------------------------------|---------------------------------------------|
| **Cross-Platform Image Support** | On-the-fly BMP conversion with header processing | Works on all Windows versions without external dependencies |
| **Connection Resilience**        | Exponential backoff algorithm with 100 retries | Survives network handoffs between WiFi/mobile |
| **Memory Efficiency**           | Streaming conversion via BytesIO            | Handles 100MB+ images without memory spikes |
| **Mobile Optimization**         | 60s timeout with keepalive packets          | Works reliably on high-latency networks     |

### 📂Project Structure
```
.
├── README.md
├── requirements.txt
├── ios_shortcuts/ # iOS shortcut
│ ├── PullClipboard.shortcut
│ ├── PushClipboard.shortcut
│ ├── AwaitUpdate.shortcut
│ ├── PullClipboardManual.md
│ ├── PushClipboardManual.md
│ └── AwaitUpdateManual.md
├── telegram_client/
│ ├── clipboard_manager.py 
│ ├── telegram_handler.py
│ └── main.py
└── screenshots/ 
```
 
## 🛠 Installation
### Windows Setup
- Install all python packages required
```bash
pip install telethon pillow python-dotenv pywin32
```
- Edit with your credentials from my.telegram.org
- - run the `ClipboardSync.py`

### iOS Configuration
- Import shortcuts from /ios_shortcuts folder
- Configure bot token and chat id in shortcut variables

## Telegram Bot & API Setup Guide

### Part 1: Creating a Telegram Bot

#### Step 1: Start with BotFather
1. Open Telegram and search for `@BotFather` (the official bot creation interface)
2. Click "Start" or send `/start` to begin

#### Step 2: Create New Bot
Send the following command to @BotFather:
`/newbot`

#### Step 3: Name Your Bot
1. Enter your bot's display name (what users will see)
   - Example: `ClipboardSync Bot`
2. Choose a unique username ending with `bot`
   - Example: `clipboard_sync_bot`
   - Note: Usernames must be 5-32 characters and globally unique

#### Step 4: Save Credentials
BotFather will respond with:
Done! Congratulations on your new bot.

Bot_Token: 123456789:ABCdefGHIJKlmNOPQRstUVWxyZ-1234567890

⚠️ **IMPORTANT**: This token gives full control over your bot. Never commit it to public repositories.

### Part 2: Obtaining Telegram API Credentials

#### Step 1: Visit API Development Tools
Go to [my.telegram.org](https://my.telegram.org) in your browser
Here's a detailed step-by-step tutorial in Markdown format for creating a Telegram bot and obtaining API credentials for Telethon:

# Telegram Bot & API Setup Guide

## Part 1: Creating a Telegram Bot

### Step 1: Start with BotFather
1. Open Telegram and search for `@BotFather` (the official bot creation interface)
2. Click "Start" or send `/start` to begin

### Step 2: Create New Bot
Send the following command to @BotFather:
/newbot


### Step 3: Follow Prompts
1. Enter your bot's display name (what users will see)
   - Example: `ClipboardSync Bot`
2. Choose a unique username ending with `bot`
   - Example: `clipboard_sync_bot`
   - Note: Usernames must be 5-32 characters and globally unique

### Step 4: Save Credentials
BotFather will respond with:
Done! Congratulations on your new bot.

Token: 123456789:ABCdefGHIJKlmNOPQRstUVWxyZ-1234567890


⚠️ **IMPORTANT**: This token gives full control over your bot. Never commit it to public repositories.

## Part 2: Obtaining Telegram Chat ID
### Step 1: Start a Chat with Your Bot
send a message to your bot in privatr chat

### Step 2: Visit the URL
visit this URL: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

### Step 3: Find Your Chat ID
Look for the chat object in the response:
"chat": {
   "id": 123456789,
   "type": "private",
   "first_name": "John",
   "last_name": "Doe",
   "username": "johndoe",
   "is_bot": false
}


## Part 3: Obtaining Telegram API Credentials
### Step 1: Visit API Development Tools
Go to [my.telegram.org](https://my.telegram.org) in your browser

### Step 2: Log In
1. Enter your registered Telegram phone number (with country code)
   - Example: `+85294931574`
2. You'll receive a login code via Telegram (not SMS)

### Step 3: Create New Application
1. Click "API development tools"
2. Fill the form with:
   - **App title**: Your project name (e.g., "Clipboard Sync")
   - **Short name**: 3-32 character identifier (e.g., "clipsync")
   - **Platform**: Typically "Desktop"
   - **Description**: Briefly explain your app's purpose

### Step 4: Get API Credentials
After submission, you'll receive:
- **api_id**: Unique numeric identifier (e.g., `1234567`)
- **api_hash**: 32-character hexadecimal string (e.g., `9cf771f2f485dac778e058b9800b2d9b`)

## Part 4: Telethon Configuration

### Required Credentials
You'll need these values for Telethon:
```python
# Load sensitive data from environment variables
API_ID = int(os.getenv('TG_API_ID', '<API_ID>'))
API_HASH = os.getenv('TG_API_HASH', '<API_HASH>')
PHONE = os.getenv('TG_PHONE', '<PHONE_NUMBER>')
```
substitute the placeholders with the actual values you obtained from BotFather and my.telegram.org.


