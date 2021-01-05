# telegram-bot-on-repl.it
This is a basic Telegram bot demo written in Python. It can be hosted on repl.it or somewhere else. This demo uses python-telegram-bot library https://github.com/python-telegram-bot/python-telegram-bot. It shows how to use markup keyboard and includes starter code to support a multilingual user interface. To interact with this bot on Telegram click the following link https://t.me/TigcoDemoBot. To create your own Telegram bot and explore many possibilities of bots follow the Installation instructions given below.

# Installation
1. Fork this repl
2. Create a telegram bot via BotFather. More info is here https://core.telegram.org/bots
3. Add a .env file. Set your bot token that you obtained from BotFather in this file like this TELEGRAM_TOKEN={your_bot_token}
3. Call the setWebHook method in the Telegram Bot API via the following url:
`https://api.telegram.org/bot{your_bot_token}/setWebhook?url={your_repl.it_url_to_send_updates_to}`. For example, the following is the webhook url for this bot `https://telegram-bot-on-replit.tigco.repl.co/webhook`
More info here https://core.telegram.org/bots/api#setwebhook
4. (Optional) For your repl to stay up and continue serving requests it needs to receive requests periodically. To achieve that you can make an account on Uptime Robot and put a monitor on your repl URL.
