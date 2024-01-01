from telebot import types
from utils.button_text import ButtonSigns


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
    add_city = types.InlineKeyboardButton("\U0001F3E1 Add city", callback_data="Add location")
    markup.row(cancel, add_city)

    return markup


def inline_cancel_btn():
    return types.InlineKeyboardButton(ButtonSigns.cancel, callback_data="Cancel")


# def inline_set_favorite_location_btn(location):
#     return types.InlineKeyboardButton(ButtonSigns.set_favorite_location, callback_data=f"Set {location}")


def inline_set_location_prompt_btn():
    return types.InlineKeyboardButton(ButtonSigns.setting_location, callback_data=f"Set prompt")


def inline_set_location_btn(to_where, location):
    return types.InlineKeyboardButton(ButtonSigns.set_favorite_location, callback_data=f"Add|{to_where}|{location}")


def inline_add_location_prompt_btn():
    return types.InlineKeyboardButton(ButtonSigns.adding_location, callback_data=f"Add prompt")


def inline_add_location_btn(to_where, location):
    return types.InlineKeyboardButton(ButtonSigns.add_wishlist_location, callback_data=f"Add|{to_where}|{location}")


def inline_change_location_prompt_btn():
    return types.InlineKeyboardButton(ButtonSigns.changing_location, callback_data=f"Change prompt")


def inline_change_location_btn(to_where, location):
    return types.InlineKeyboardButton(ButtonSigns.change_favorite_location, callback_data=f"Add|{to_where}|{location}")


def inline_empty_wishlist_btn():
    return types.InlineKeyboardButton(ButtonSigns.clear_wishlist, callback_data="Clear wishlist")
