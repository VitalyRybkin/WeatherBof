from telebot import types

import data
from keyboards.inline.inline_buttons import inline_cancel_btn
from loader import bot
from states.bot_states import States


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
