# Pull Clipboard from TelegramBot
## Description
This shortcut allows you to receive the contents of your clipboard from a specific telegram bot. It checks if the received content is text or photo, and handles it accordingly.
## Requirements
- Telegram bot token

## Code and comments
*// run and recieve the result from another shortcut, tmp is a dictionary*
🚀 **Run** `🔧awaitUpdate`  
🔤 **Set variable** `tmp` **to** `🚀 Shortcut Result`  
*// if tmp has text value, copied text value to clipboard*
📚 **Get** `value` **for** `text` **in** `🔤tmp`  
🔀 **If** `📚Dictionary Value` `has any value`
&emsp;📑 **Copy** `📚Dictionary Value` **to clipboard** 
&emsp;🔔 **Show notification** `Text copied: 📚Dictionary Value`  
*// otherwise, tmp contains a photo, download it and add to clipboard*
🔀 **Otherwise**
&emsp;📚 **Get** `Value` **for** `photo` **in** `🔤tmp`  
&emsp;📜 **Get** `Last Item` **from** `📚Dictionary Value`  
&emsp;📚 **Get** `Value` **for** `file_id` **in** `📜item from list`  
&emsp;🔢 **Set variable** `fileid` **to** `📚Dictionary Value`  
&emsp;📥 **Get contents of** `https://api.telegram.org/bot<BOT_TOKEN>/getFile?file_id=🔢fileid`
&emsp;📚 **Get** `Value` **for** `result` **in** `📥Contents of URL`
&emsp;📚 **Get** `Value` **for** `file_path` **in** `📚Dictionary Value`
&emsp;📥 **Get contents of** `https://api.telegram.org/file/bot<BOT_TOKEN>/📚Dictionary Value`
&emsp;📑 **Copy** `📚Dictionary Value` **to clipboard** 
&emsp;🔔 **Show notification** `image successfully copied`
🔀 **End If**

## Notes
- pull a file from the computer's clipboard is not supported, because the author believe that it is not a common use case.
- The shortcut is designed to be runned manually, but you can add it to the home screen or the Control Centre to make it more accessible.
