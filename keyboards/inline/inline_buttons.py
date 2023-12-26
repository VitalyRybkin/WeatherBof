from telebot import types


def show_weather():
    markup = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton("\U0000274C Cancel", callback_data="Cancel")
    stop = types.InlineKeyboardButton(
        "\U0001F324 Forecast?", callback_data="Show weather"
    )
    markup.row(check, stop)

    return markup


def inline_add_button():
    markup = types.InlineKeyboardMarkup()
    cancel = types.InlineKeyboardButton("\U0000274C Cancel", callback_data="Cancel")
    add_city = types.InlineKeyboardButton("\U0001F3E1 Add city", callback_data="Add city")
    markup.row(cancel, add_city)

    return markup
