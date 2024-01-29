from telebot import types

from midwares.sql_lib import Current, Hourly, Daily
from utils.button_text import ButtonSigns


def show_weather():
    markup = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton("\U0000274C Cancel", callback_data="Cancel")
    stop = types.InlineKeyboardButton(
        "\U0001F324 Forecast?", callback_data="Show weather"
    )
    markup.row(check, stop)

    return markup


def inline_cancel_btn():
    return types.InlineKeyboardButton(ButtonSigns.cancel, callback_data="Cancel")


def inline_exit_btn():
    return types.InlineKeyboardButton(ButtonSigns.exit, callback_data="Exit")


def inline_set_location_prompt_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.setting_location, callback_data=f"Set prompt"
    )


def inline_set_location_btn(to_where: str, loc_id: str):
    return types.InlineKeyboardButton(
        ButtonSigns.set_favorite_location, callback_data=f"Add|{to_where}|{loc_id}"
    )


def inline_add_location_prompt_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.adding_location, callback_data=f"Add prompt"
    )


def inline_add_location_btn(to_where: str, loc_id: str):
    return types.InlineKeyboardButton(
        ButtonSigns.add_wishlist_location, callback_data=f"Add|{to_where}|{loc_id}"
    )


def inline_set_wishlist_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.set_wishlist, callback_data=f"Change wishlist"
    )


def inline_change_location_prompt_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.changing_location, callback_data=f"Change prompt"
    )


def inline_change_location_btn(to_where: str, loc_id: str):
    return types.InlineKeyboardButton(
        ButtonSigns.change_favorite_location, callback_data=f"Add|{to_where}|{loc_id}"
    )


def inline_empty_wishlist_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.clear_wishlist, callback_data="Clear wishlist"
    )


def inline_current_weather_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.current, callback_data=f"{Current.table_name}_display"
    )


def inline_hourly_weather_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.hourly_weather, callback_data=f"{Hourly.table_name}_display"
    )


def inline_daily_weather_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.daily_weather, callback_data=f"{Daily.table_name}_display"
    )


def inline_current_settings_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.current_weather, callback_data="Current settings"
    )


def inline_hourly_settings_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.hourly_weather, callback_data="Hourly settings"
    )


def inline_daily_settings_btn():
    return types.InlineKeyboardButton(
        ButtonSigns.daily_weather, callback_data="Daily settings"
    )


def inline_change_settings_btn(which):
    return types.InlineKeyboardButton(
        ButtonSigns.change_favorite_location, callback_data=f"Change|{which}"
    )


def inline_save_settings_btn(which):
    return types.InlineKeyboardButton(
        ButtonSigns.save_settings, callback_data=f"Save|{which}"
    )
