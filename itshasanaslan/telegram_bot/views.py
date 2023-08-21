from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import threading
import os
import json
import os
from telegram.ext import *
from telegram import Poll, Update, ReplyKeyboardRemove
from .Helpers import *


BOT_WORKS = False
API_KEY = "1687839843:AAFuaSiLCI_BGJroVYukYqjrh_4skNTNBFw"


def telegram_main_page(request):
    global BOT_WORKS
    return HttpResponse("<html><head></head><body><center><h1>KPSS bittiği için kapalıyız...<br>Promosyon3</h1></body></html>")
    if not BOT_WORKS:
        BOT_WORKS = True
        start_main = threading.Thread(target=main)
        start_main.start()
    return  HttpResponse("Works")



#print("Bot is running...")
CLEAR_CONSOLE_CODE = "cls"
CURRENT_GROUP = None
drive_api = DriveAPI()
quiz_controller = QuizHandler()
telegram_control = TelegramControl(API_KEY, drive_api, quiz_controller)


def start_command(update, context):
    update.message.reply_text("If you don't know who I am, please do not interfere.")


def help_command(update, context):
    global telegram_control
    update.message.reply_text('Ask questions to @itshasanaslan!')
    msg = "KOMUTLAR\n"
    num = 1
    for i,j in telegram_control.help_commands.items():
        msg += str(num) + ")" + i + ": " +  j + "\n\n"
        num += 1
    update.message.reply_text(msg)


def handle_message(update, context):
    global telegram_control
    text = str(update.message.text).lower()
    #update.message.reply_text("Üzgünüm, o devir bitti...")
    if update.message.reply_to_message:
        telegram_control.manage_reply_text(update, context)
    telegram_control.console_interface(update)
    #response = R.sample_responses(text)
    #if response != "0":
        #update.message.reply_text(response)
        #pass
    #update.message.reply_text("Ben çekileyim abla")


def receive_poll(update: Update, context: CallbackContext) -> None:
    global telegram_control
    #actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for
    # a closed poll
    """update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed=True,
        reply_markup=ReplyKeyboardRemove(),
    )"""
    #for property,value in vars(update).items():print(property,value,"\n")
    #print(update.message.poll)
    #print(update.message.from_user)
    #print(actual_poll)
    alert = telegram_control.quiz_controller.increase(update.message.from_user)
    if alert:
        update.message.reply_text(alert)
    print(telegram_control.quiz_controller.quiz_senders_info)

def error(update, context):
    global telegram_control
    print(f"Update {update} caused error:\n {context.error}\n\n")
    

    
def main():
    global API_KEY
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.poll, receive_poll))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()



    
