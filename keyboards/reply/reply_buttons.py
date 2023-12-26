from telebot import types
from utils.signs_text import ButtonSigns


def reply_set_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    set_city = types.KeyboardButton(ButtonSigns.set_city)
    cancel = types.KeyboardButton(ButtonSigns.cancel)
    markup.add(set_city, cancel)

    return markup


def reply_cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    cancel = types.KeyboardButton(ButtonSigns.cancel)
    markup.add(cancel)

    return markup
