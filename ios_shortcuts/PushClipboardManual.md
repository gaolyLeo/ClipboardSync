# Push Clipboard to Telegram
## Description
This shortcut allows you to share the contents of your clipboard to a sepecific telegram bot. It checks if the clipboard is empty, and if not, it determines the type of content (text or photo) and sends it accordingly.
Each message containing the clipboard content is prefixed with `/push` to trigger `process_push` defined in the Python program.
## Requirements
- Telegram bot token
- Telegram chat ID (fetched using getUpdates)
## Code and comments

📋 **Get Clipboard** 
*// alert the user if the clipboard is empty*
🔀 **If** `📋 Clipboard` `has no value`
&emsp;⚠️ **Show Alert**: `"Clipboard is empty!"`  
&emsp;⏹️ **Stop This Shortcut**  
🔀 **End If**  
*// check the type of content in the clipboard*
⚙️ **Get Type of** `📋 Clipboard`  
*// if the clipboard contains photo media, convert it to JPEG*
🔀 **If** `⚙️Type` `is` `Photo media` 
&emsp;🖼️ **Convert** `📋 Clipboard` **to** `JPEG`  
*// send the photo to telegram bot* 
&emsp;📥 **Get Contents of**: `https://api.telegram.org/bot<BOT_TOKEN>/sendPhoto`  
&emsp;&emsp;Method: `POST`  
&emsp;&emsp;Request Body: `Form` 
&emsp;&emsp;{
&emsp;&emsp;&emsp;chat_id: `<CHAT_ID>`
&emsp;&emsp;&emsp;caption: `/push`
&emsp;&emsp;&emsp;photo: `📋Clipboard`  
&emsp;&emsp;}
*// if the clipboard contains text, send it as a message*
🔀 **Otherwise**
&emsp;📥 **Get Contents of** `https://api.telegram.org/bot<BOT_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=/push📋Clipboard`  
🔀 **End If**  
🔔 **Show notification** `Clipboard successfully shared`

## Notes
- The condition where clipboard contains a file is not handled properly, because the author believe that it is not a common use case.
- In IOS shortcut, there are many types that should be treated as text, such as URL, email, phone number, etc. So all the these types are handled in the otherwise branch. 
- The shortcut is designed to be runned manually, but you can add it to the home screen or the Control Centre to make it more accessible.


