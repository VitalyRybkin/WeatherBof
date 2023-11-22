from telebot import types


def show_weather():
    markup = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton('\U0001F324 Check weather')
    stop = types.InlineKeyboardButton('\U0000274C Cancel')
    markup.row(check, stop)

    return markup


def add_button():
    markup = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton('\U0000274C Cancel', callback_data='Cancel')
    stop = types.InlineKeyboardButton('\U0001F3E1 Add city', callback_data='Add_city')
    markup.row(check, stop)

    return markup

