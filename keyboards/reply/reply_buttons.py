from telebot import types


def reply_set_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    set_city = types.KeyboardButton('\U0001F3E1 Set city')
    cancel = types.KeyboardButton('\U0000274C Cancel')
    markup.add(set_city, cancel)

    return markup


def reply_cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    cancel = types.KeyboardButton("\U0000274C Cancel")
    markup.add(cancel)

    return markup
