from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_add_location_prompt_btn, \
    inline_set_wishlist_btn
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Favorite, User
from states.bot_states import States


@bot.message_handler(commands=["change"])
@bot.message_handler(state=States.change_wishlist)
def get_wishlist(message) -> None:
    """
    Function. Executes change command. Change wishlist prompt. Setting change_wishlist state.
    :param message:
    :return:
    """
    print("change : ", bot.get_state(message.from_user.id, message.chat.id))
    if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0
            and not bot.get_state(message.from_user.id, message.chat.id) == States.change_wishlist):
        bot.edit_message_reply_markup(
            message.chat.id,
            message_id=data.globals.users_dict[message.from_user.id]['message_id'],
            reply_markup="")

    query = (
        f"SELECT {Favorite.user_favorite_city_name} "
        f"FROM {Favorite.table_name} "
        f"WHERE {Favorite.favorite_user_id}="
        f"({User.get_user_id(message.from_user.id)})"
        f"ORDER BY {Favorite.user_favorite_city_name}"
    )
    get_wishlist_data = read_data(query)

    if get_wishlist_data:
        States.change_wishlist.wishlist = {}
        for loc in get_wishlist_data:
            States.change_wishlist.wishlist[loc[0]] = True

        markup = types.InlineKeyboardMarkup()
        for loc, isSet in States.change_wishlist.wishlist.items():
            if isSet:
                markup.add(types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove|{loc}"))
        markup.row(inline_set_wishlist_btn())
        markup.row(inline_cancel_btn())
        msg = bot.send_message(message.chat.id, "Tap location name to remove from wishlist:", reply_markup=markup)

        bot.set_state(message.from_user.id, States.change_wishlist, message.chat.id)

    else:
        markup = types.InlineKeyboardMarkup()
        add_location = inline_add_location_prompt_btn()
        cancel = inline_cancel_btn()
        add_city_menu = markup.row(add_location, cancel)
        msg = bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)

    data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id
    print("change : ", bot.get_state(message.from_user.id, message.chat.id))
