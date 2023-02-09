import os
# from constants import API_KEY
import re
import pytz
import logging
from weather_data import access_last_city
from telegram.ext import *
from tele_modules import is_it_raining
from telegram.ext import Updater, CommandHandler
from telegram import Update
import datetime


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

API_KEY = os.environ.get("API_KEY")
CHAT_ID = ""
# TAYMER = datetime.time(hour=int(18), minute=int(40), tzinfo=pytz.timezone('Europe/Ljubljana'))


def start(update, context):
    update.message.reply_text("Rainy 🐼 Bot Is Here To Help.\n"
                              "If you need help with controlling the bot type '/help' in the chat.")


def help_msg(update, context):
    update.message.reply_text(f"Im here to help.\nTo change the location type e.g. '/change London, GB'"
                              f"\nTo see current location type '/location'\n")


def change(update: Update, context: ContextTypes.context) -> None:
    text = context.args
    try:
        if len(text) > 1:
            new_text = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in text]
            output = f"{new_text[0].title()},{new_text[1].upper()}"
            with open("country_codes.txt", "a") as myfile:
                myfile.write(f"{output}\n")
            update.message.reply_text(f"City has been changed to {access_last_city()}"
                                      f" and weather data for today is: {is_it_raining()}")
        elif len(text) == 1:
            new_text = text[0].split(",")
            output = f"{new_text[0].title()},{new_text[1].upper()}"
            with open("country_codes.txt", "a") as myfile:
                myfile.write(f"{output}\n")
            update.message.reply_text(f"City has been changed to {access_last_city()}"
                                      f" and weather data for today is: {is_it_raining()}")
    except IndexError:
        update.message.reply_text(
            f"You have typed /change command wrong")


def weather(update, context):
    update.message.reply_text(is_it_raining())


def location(update, context):
    update.message.reply_text(access_last_city())


def send_message_job(context):
    context.bot.send_message(chat_id=CHAT_ID, text=f"{is_it_raining()}")


def remove_job_if_exists(name: str, context: ContextTypes.context) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_time(update: Update, context: ContextTypes.context) -> None:
    try:
        global CHAT_ID
        CHAT_ID = update.effective_message.chat_id
        alarm = context.args[0].split(":")
        a1 = alarm[0]
        a2 = alarm[1]

        job_removed = remove_job_if_exists(str(CHAT_ID), context)

        timer = datetime.time(hour=int(a1), minute=int(a2), tzinfo=pytz.timezone('Europe/Ljubljana'))
        context.job_queue.run_daily(send_message_job, timer, name=str(CHAT_ID))
        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text("You typed /set command wrong.")


def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_msg))
    dp.add_handler(CommandHandler("change", change))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("location", location))
    dp.add_handler(CommandHandler("set", set_time))

    updater.start_polling()
    updater.idle()


main()
