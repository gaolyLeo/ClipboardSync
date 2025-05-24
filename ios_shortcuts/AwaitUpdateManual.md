# Await the Latest Updates
## Description
This shortcut allows you to check for the latest updates from a Telegram bot. It sends out a /pull request first and continuously checks the latest the updates, until it finds a new message sent within 10 seconds or /pull request failed. The shortcut will stop and output the latest message dictionary if found, or show an alert if there is a network error.
## Requirements
- Telegram bot token
- Telegram chat ID (fetched using getUpdates)
## Code and comments
*// send /pull request to the computer*
📥 **Get Contents of** `https://api.telegram.org/bot<BOT_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=📋Clipboard` 
*// check if the request was successful* 
🔄 **Repeat** `10 times`
&emsp;📥 **Get Contents of**: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
&emsp;📚 **Get** `Value` **for** `result` **in** `📥Contents of URL`
&emsp;📜 **Get** `Last Item` **from** `📚Dictionary Value`  
&emsp;📚 **Get** `Value` **for** `message` **in** `📜item from list`  
&emsp;🔤 **Set variable** `res` **to** `📚Dictionary Value`  
&emsp;📚 **Get** `Value` **for** `date` **in** `🔤res`  
*// get the timestamp of current time*
&emsp;📅 **Get** `Seconds` **between** `1970/1/1 08:00` **and** `📅Current Date`
*// get the time difference between the current date and the date of the message*
&emsp;🧮 `📅Time between Dates` **-** `📚Dictionary Value`
*// check if the time difference is less than 10 seconds, which means the received message is the latest*
&emsp;🔀 **If** `🧮Calculate Result` **is less than** `10`
&emsp;&emsp;⏹️ **Stop and output** `🔤res`
&emsp;🔀 **End If**
&emsp;🕐 **Wait** `1 second`
🔀 **End Repeat**
⚠️ **Show Alert**: `Newwork error!`  

## Notes
- The shortcut won't be runned manually, but runned by the PullClipboard shortcuts
- The concrete time of when timestamp begins should be set according to your timezone.
- 

