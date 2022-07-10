import configparser as cf
import telebot
import os
from detect import detect_objects
import re

# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

# set of user ids with enabled debug mode
debug = set()

# Reading config
secretConfig = cf.ConfigParser()
secretConfig.read_file(open('secret.cfg'))
api_token = secretConfig.get('TELEGRAM', 'API_TOKEN')

# creating bot
bot = telebot.TeleBot(api_token, parse_mode=None)


# Handling Telegram commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image and I detect objects on it")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image and I detect objects on it.")


@bot.message_handler(commands=['debug'])
def send_message(message):
    global debug
    user_id = message.from_user.id
    if user_id in debug:
        debug.discard(user_id)
        debug_is = 'Off'
    else:
        debug.add(user_id)
        debug_is = 'On'
    bot.reply_to(message, "Debug is " + debug_is)
    # print(debug)


@bot.message_handler(commands=['trh'])
def send_message(message):
    print(message.text)
    trh = message.text.replace(",", ".")
    print(trh)
    trh = re.findall("\d+\.\d+", trh)
    print(trh)
    if len(trh) > 0:
        trh = float(trh[0])
        print(trh)
        if trh > 0 and trh < 1:
            bot.reply_to(message, str(trh))
            return

    bot.reply_to(message, "Set objects detection threshold between 0 and 1. Usage: /trh 0.4")


@bot.message_handler(content_types=["photo"])
def send_message(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    file_name = file_info.file_path.replace("/", "_")
    with open(file_name, 'wb') as new_file:
        new_file.write(file)
    result = detect_objects(file_name)
    bot.send_photo(message.chat.id, result, reply_to_message_id=message.message_id)
    # sending additional info if user enabled debug mode
    if user_id in debug:
        bot.reply_to(message, f'There are no additional debug info', parse_mode='html')
    # removing image
    try:
        os.remove(file_name)
    except:
        print("Can't delete file: " + file_name)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "This is not a photo, send me a photo")


bot.infinity_polling()
