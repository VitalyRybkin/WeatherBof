from telebot import types

from handlers.users.preferences import (
    customize_current_setting,
    customize_daily_setting,
    customize_hourly_setting,
    change_settings,
)
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_set_wishlist_btn
from loader import bot
from midwares.db_conn_center import write_data, read_data, read_data_row
from midwares.sql_lib import User, Favorite, Daily, Current, Hourly
from states.bot_states import States
import data.globals


@bot.callback_query_handler(func=lambda call: call.data in ["Cancel", "Exit"])
def cancel(call) -> None:
    """
    Function. Cancelling current bot state.
    :param call:
    :return:
    """
    bot.delete_state(call.from_user.id, call.message.chat.id)
    if call.data == "Cancel":
        bot.send_message(call.message.chat.id, "\U0000274C Canceled!")
    elif call.data == "Exit":
        bot.send_message(call.message.chat.id, "\U00002B05 Exited!")

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(
    func=lambda call: call.data == "Set prompt"
                      or call.data == "Add prompt"
                      or call.data == "Change prompt"
)
def prompt(call) -> None:
    """
    Function. 'Type in location name' - message output.
    :param call:
    :return:
    """
    bot.set_state(call.from_user.id, States.search_location, call.message.chat.id)
    States.search_location.operation = call.data
    markup = types.InlineKeyboardMarkup()
    cancel_keyboard = markup.row(inline_cancel_btn())
    msg = bot.send_message(
        call.message.chat.id,
        "\U0001F524 Type in location name:",
        reply_markup=cancel_keyboard,
    )
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id


@bot.callback_query_handler(func=lambda call: call.data == "Clear wishlist")
def clear_wishlist(call) -> None:
    """
    Function. Clearing wishlist.
    :param call:
    :return:
    """
    query = (
        f"DELETE FROM {Favorite.table_name} "
        f"WHERE {Favorite.favorite_user_id}="
        # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
        f"({User.get_user_id(call.from_user.id)})"
    )
    write_data(query)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    # bot.send_message(call.message.chat.id, "Your /wishlist is empty! /add location?")
    bot.send_message(
        call.message.chat.id, "\U00002705 Your wishlist is empty now! /add location?"
    )
    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: call.data == "Change wishlist")
def change_wishlist(call) -> None:
    """
    Function. Changing wishlist content.
    :param call:
    :return:
    """
    for loc, isSet in States.change_wishlist.wishlist.items():
        if not isSet:
            query = (
                f"DELETE FROM {Favorite.table_name} "
                f"WHERE {Favorite.user_favorite_city_name}='{loc}' "
                f"AND {Favorite.favorite_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            write_data(query)
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    bot.send_message(call.message.chat.id, "New /wishlist was set!")
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: "Remove" in call.data)
def remove_from_wishlist(call) -> None:
    """
    Function. Removing item from wishlist (created class dict) while in change_wishlist state.
    :param call:
    :return:
    """
    parse_call_data = call.data.split("|")
    States.change_wishlist.wishlist[parse_call_data[1]] = False
    markup = types.InlineKeyboardMarkup()
    for loc, isSet in States.change_wishlist.wishlist.items():
        if isSet:
            markup.add(
                types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove|{loc}")
            )
    markup.row(inline_set_wishlist_btn())
    markup.row(inline_cancel_btn())

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: "Add" in call.data)
def callback_query(call) -> None:
    """
    Function. Adding location to a wishlist or set as favorite.
    :param call:
    :return:
    """
    parse_call_data = call.data.split("|")

    if parse_call_data[1] == "favorite":
        bot.send_message(call.message.chat.id, "\U00002705 Favorite location set!")
        query = (
            f"UPDATE {User.table_name} "
            f"SET {User.user_city}='{parse_call_data[2]}' "
            f"WHERE {User.user_id}={call.from_user.id}"
        )
        write_data(query)
    elif parse_call_data[1] == "wishlist":
        query = (
            f"SELECT {Favorite.user_favorite_city_name} "
            f"FROM {Favorite.table_name} "
            f"WHERE {Favorite.favorite_user_id}="
            # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
            f"({User.get_user_id(call.from_user.id)}) "
            f"AND {Favorite.user_favorite_city_name}='{parse_call_data[2]}'"
        )
        get_wishlist_info = read_data(query)

        if not get_wishlist_info:
            bot.send_message(
                call.message.chat.id, "\U00002705 Location added to wishlist!"
            )
            # bot.answer_callback_query(call.id, show_alert=True, text="Location added to wishlist!")
            query = (
                f"INSERT INTO {Favorite.table_name} "
                f"({Favorite.favorite_user_id}, {Favorite.user_favorite_city_name}) "
                f"VALUES ((SELECT {User.id} FROM {User.table_name} "
                f"WHERE {User.user_id}={call.from_user.id}), '{parse_call_data[2]}')"
            )
            write_data(query)

            query = (
                f"SELECT {User.user_city} "
                f"FROM {User.table_name} "
                f"WHERE {User.user_id}={call.from_user.id} "
                f"AND {User.user_city}='{parse_call_data[2]}'"
            )
            get_favorite_location = read_data(query)
            if get_favorite_location:
                bot.send_message(
                    call.message.chat.id,
                    "\U00002705 This location used to be set as favorite too!",
                )
        else:
            bot.send_message(
                call.message.chat.id, "\U00002757 Location is in your wishlist!"
            )
            markup = types.InlineKeyboardMarkup()
            cancel_keyboard = markup.row(inline_cancel_btn())
            msg = bot.send_message(
                call.message.chat.id,
                "\U00002328 Type in location name:",
                reply_markup=cancel_keyboard,
            )
            bot.edit_message_reply_markup(
                call.message.chat.id,
                message_id=data.globals.users_dict[call.from_user.id]["message_id"],
                reply_markup="",
            )
            data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id
            return

    bot.delete_state(call.from_user.id, call.message.chat.id)

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(
    func=lambda call: call.data
                      in ["Current settings", "Daily settings", "Hourly settings"]
)
def current_settings(call) -> None:
    """
    Function. Change state, call next step.
    :param call:
    :return:
    """

    match call.data:
        case "Current settings":
            bot.set_state(
                call.from_user.id, States.customize_current, call.message.chat.id
            )
            States.customize_current.user_id = call.from_user.id
            settings = (
                "<b>\U0001F4C2 Current weather settings:</b>\n\n"
                "\U0001F4C4 <b>Default output:</b>\n"
                "       - temperature;\n"
                "       - 'feels like' temperature;\n"
                "       - wind;\n"
                "       - clouds; \n"
                "       - precipitations;"
            )

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Current.humidity}, {Current.pressure}, {Current.visibility}, {Current.wind_extended} "
                f"FROM {Current.table_name} "
                f"WHERE {Current.current_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_current.settings_dict = read_data_row(query)
            customize_current_setting(call.message)
        case "Daily settings":
            bot.set_state(
                call.from_user.id, States.customize_daily, call.message.chat.id
            )
            States.customize_daily.user_id = call.from_user.id

            settings = ("<b>\U0001F4C2 Daily weather settings:</b>\n\n"
                        "\U0001F4C4 <b>Default output:</b>\n"
                        "       - max temperature;\n"
                        "       - min temperature;\n"
                        "       - average temperature;\n"
                        "       - max wind;\n"
                        "       - total precipitations;\n"
                        "       - chance of rain;\n"
                        "       - chance of snow;\n")

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Daily.humidity}, {Daily.visibility}, {Daily.astro} "
                f"FROM {Daily.table_name} "
                f"WHERE {Daily.daily_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_daily.settings_dict = read_data_row(query)
            customize_daily_setting(call.message)
        case "Hourly settings":
            bot.set_state(
                call.from_user.id, States.customize_hourly, call.message.chat.id
            )
            States.customize_hourly.user_id = call.from_user.id
            settings = ("<b>\U0001F4C2 Hourly weather settings:</b>\n\n"
                        "\U0001F4C4 <b>Default output:</b>\n"
                        "       - temperature;\n"
                        "       - 'feels like' temperature;\n"
                        "       - wind;\n"
                        "       - clouds; \n"
                        "       - chance of rain;\n"
                        "       - chance of snow;\n"
                        "       - precipitations;\n")

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Hourly.humidity}, {Hourly.pressure}, {Hourly.visibility}, {Hourly.wind_extended} "
                f"FROM {Hourly.table_name} "
                f"WHERE {Hourly.hourly_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_hourly.settings_dict = read_data_row(query)
            customize_hourly_setting(call.message)


@bot.callback_query_handler(func=lambda call: "Change" in call.data)
def change_setting(call):
    parse_call_data = call.data.split("|")
    bot.set_state(call.from_user.id, States.change_setting, call.message.chat.id)
    States.change_setting.user_id = call.from_user.id
    States.change_setting.setting = parse_call_data[1]

    change_settings(call.message)


@bot.callback_query_handler(func=lambda call: "Switch setting" in call.data)
def switch_setting(call):
    parse_call_data = call.data.split("|")
    match parse_call_data[1]:
        case Current.table_name:
            States.customize_current.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_current.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )
        case Hourly.table_name:
            States.customize_hourly.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_hourly.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )
        case Daily.table_name:
            States.customize_daily.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_daily.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )

    bot.delete_message(
        call.message.chat.id, data.globals.users_dict[call.from_user.id]["message_id"]
    )
    data.globals.users_dict[call.from_user.id]["message_id"] = 0
    change_settings(call.message)


@bot.callback_query_handler(func=lambda call: "Save" in call.data)
def save_settings(call):
    parse_call_data = call.data.split("|")
    table_name = fields = ''
    match parse_call_data[1]:
        case Current.table_name:
            table_name = Current.table_name
            for k, v in States.customize_current.settings_dict[0].items():
                fields += k + f'={v}, '
        case Hourly.table_name:
            table_name = Hourly.table_name
            for k, v in States.customize_hourly.settings_dict[0].items():
                fields += k + f'={v}, '
        case Daily.table_name:
            table_name = Daily.table_name
            for k, v in States.customize_daily.settings_dict[0].items():
                fields += k + f'={v}, '

    fields = fields[:-2]
    query = (
        f"UPDATE {table_name} "
        f"SET {fields} "
        f"WHERE {table_name + '_user_id'}="
        # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
        f"({User.get_user_id(call.from_user.id)})"
    )
    write_data(query)
