import data
from loader import bot


@bot.callback_query_handler(func=lambda call: call.data in ["Cancel", "Exit"])
def cancel(call) -> None:
    """
    Function. Cancelling or exiting current bot state.
    :param call:
    :return:
    """
    bot.delete_state(call.from_user.id, call.message.chat.id)

    if call.data == "Cancel":
        bot.send_message(call.message.chat.id, "\U0000274C Canceled!")
    elif call.data == "Exit":
        bot.send_message(call.message.chat.id, "\U00002B05 Exited!")

    if not data.globals.users_dict[call.from_user.id]["message_id"] == 0:
        bot.edit_message_reply_markup(
            call.message.chat.id,
            message_id=data.globals.users_dict[call.from_user.id]["message_id"],
            reply_markup="",
        )
        data.globals.users_dict[call.from_user.id]["message_id"] = 0

    if data.globals.users_dict[call.from_user.id]["message_list"]:
        for msg in data.globals.users_dict[call.from_user.id]["message_list"]:
            bot.delete_message(call.message.chat.id, msg)
        data.globals.users_dict[call.from_user.id]["message_list"] = []
