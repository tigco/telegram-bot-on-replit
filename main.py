#!/usr/bin/env python

"""Demo Telegram bot on repl.it.

This program is dedicated to the public domain under the MIT License.
"""
from flask import Flask, request, render_template
app = Flask(__name__)

import logging
import os
from datetime import datetime, timezone

from telegram import (
  Bot,
  ChatAction,
  KeyboardButton,
  ParseMode,
  ReplyKeyboardMarkup,
  Update,
  )

# Only english language for now. Commenting out the Russian dictionary.
# import i18ndict.ru as ru_lang
import i18ndict.en as en_lang
# Set English as the default bot UI language
bot_lang = en_lang

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define global vars and constants
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))


def start():
    """Start and restart handler. Checks what additional information is necessary and acts accordingly.
    Args:
        update: an incoming Telegram update.
    Returns:
        None;
    """
    logger.info("In start handler.")

    # Example of retrieving the username from an incoming Telegram update.
    user_data = {}
    if update.message.from_user.username:
        user_data['username'] = update.message.from_user.username
        logger.info('Username {}'.format(user_data['username']))
    
    # Display keyboard
    build_keyword_selector()


def build_keyword_selector():
    """Build a custom keyboard to make interacting with the bot easier.
    Args:
        update: an incoming Telegram update.
    Returns:
        None;
    """
    # Add buttons to a row of keys
    keyboard_row_1 = [
      KeyboardButton(bot_lang.show_time_lon_cmd),
      KeyboardButton(bot_lang.nothing_cmd),
    ]
    keyboard_row_2 = [
      KeyboardButton(bot_lang.throw_1_dice_cmd),
      KeyboardButton(bot_lang.throw_2_dice_cmd),
    ]
    keyboard = [
      keyboard_row_1,
      keyboard_row_2,
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, True)

    if update.effective_chat:
        bot.send_message(chat_id=update.effective_chat.id, 
                        text=bot_lang.choose_command_msg, 
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup)


def keyboard_handler():
    """Method to handle user selections on the custom keyboard.
    Args:
        update: an incoming Telegram update.
    Returns:
        None;
    """
    logger.info(f"In keyboard handler. Message text: {update.message.text}")
    
    if update.effective_chat:
      if update.message.text == bot_lang.show_time_lon_cmd:
        bot.send_message(chat_id=update.effective_chat.id, text=get_time(timezone.utc))
      elif update.message.text == bot_lang.throw_1_dice_cmd:
        # '\U0001F3B2' is the python encoding for the unicode character game dice 
        bot.send_dice(chat_id=update.effective_chat.id, emoji='\U0001F3B2')
      elif update.message.text == bot_lang.throw_2_dice_cmd:
        bot.send_dice(chat_id=update.effective_chat.id, emoji='\U0001F3B2')
        bot.send_dice(chat_id=update.effective_chat.id, emoji='\U0001F3B2')
      else:
        bot.send_message(chat_id=update.effective_chat.id, text='Doing nothing...')


def timeout(message):
    """Check whether it has not been too long since the last message.
    Helpful to avoid handling the same request that cannot be handled
    because of a bug in the code.
    Args:
        update: an incoming Telegram update.
        message: a message from the Telegram update.
    Returns:
        True or False.
    """
    event_age_ms = get_message_age(message)
    # Ignore events that are too old
    max_age_ms = 30000
    if event_age_ms < max_age_ms:
        return False
    else:
        if update.effective_chat:
            bot.send_message(chat_id=update.effective_chat.id, text=bot_lang.thought_you_left_msg)
        logger.info('Dropped {} (age {}ms)'.format(update.update_id, event_age_ms))
        return True


def get_message_age(message):
    """Compute the time since the last message first arrived.
    Args:
        message: a message from the Telegram update.
    Returns:
        message age in milliseconds.
    """
    event_time = message.date
    if message.edit_date:
        event_time = message.edit_date
    event_age = (datetime.now(timezone.utc) - event_time).total_seconds()
    event_age_ms = event_age * 1000
    logger.info(str(event_age_ms))
    return event_age_ms


def get_time(local_timezone = timezone.utc):
  return datetime.now(local_timezone).strftime("%d-%b-%Y (%H:%M:%S)")


# Optional. Strictly speaking the decorator and function below code are not necessary for the
# bot to work.
# However, I recommend keeping this code. It lets us have the landing/status page (index.html) 
# for the bot. Additonally, we're using Uptime Robot to keep the bot up. If this code is
# removed, Uptime Robot will receive 404 response when pinging the '/' route and report it as down. 
@app.route('/')
def index():
  return render_template("index.html")


# The bot entry point. Telegram send HTTPS POST request whenever there is an update for the bot.
# Therefore, we only accept the POST method. 
@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook for the telegram bot.
    Args:
        request: A flask.Request object.
    Returns:
        Response text.
    """

    logger.info("In webhook handler")
    global bot_lang

    if request.method == "POST":
        global update
        update = Update.de_json(request.get_json(force=True), bot)

        # your bot can receive updates without messages
        if update.message:
            if timeout(update.message):
                return "Timeout"
            bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            if update.message.text in ("/start", "/Start"):
                start()
                return "ok"

            # default
            keyboard_handler()
            return "ok"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8443)

