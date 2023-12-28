from telebot import types
from utils.button_text import ButtonSigns


def reply_set_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    set_city = types.KeyboardButton(ButtonSigns.setting_location)
    cancel = types.KeyboardButton(ButtonSigns.cancel)
    markup.add(set_city, cancel)

    return markup


def reply_cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    cancel = types.KeyboardButton(ButtonSigns.cancel)
    markup.add(cancel)

    return markup


def reply_cancel_btn():
    return types.KeyboardButton(ButtonSigns.cancel)


def reply_set_btn():
    return types.KeyboardButton(ButtonSigns.setting_location)


def reply_add_favorite_btn():
    return types.KeyboardButton(ButtonSigns.set_favorite_location)
