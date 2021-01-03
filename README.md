# telegram-bot-on-repl.it
This is a basic Telegram bot written in Python. It can be hosted on repl.it or somewhere else. This demo uses python-telegram-bot library https://github.com/python-telegram-bot/python-telegram-bot. It showshow to use markup keyboard and includes starter code to support multilingual user interface.

# Installation
1. Fork this repl
2. Create a telegram bot via BotFather. More info is here https://core.telegram.org/bots
3. Add a .env file. Set your bot token that you obtained from BotFather in this file like this TELEGRAM_TOKEN={your_bot_token}
3. Call the setWebHook method in the Telegram Bot API via the following url:
https://api.telegram.org/bot{your_bot_token}/setWebhook?url={your_repl.it_url_to_send_updates_to}.
More info here https://core.telegram.org/bots/api#setwebhook
4. (Optional) For your repl to stay up and continue serving requests it needs to receive requests periodically. You can make an account on Uptime Robot and put a monitor on your repl URL.
