from telebot import types


def reply_add_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("\U0001F3E1 Add city")
    btn2 = types.KeyboardButton("\U0000274C Cancel")
    markup.add(btn1, btn2)

    return markup
