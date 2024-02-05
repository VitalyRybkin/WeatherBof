from telebot.types import Message

import data
from loader import bot


def update_msg_id(message, new_msg: Message) -> None:
    """
    Function. Update user message id to edit or delete.
    :param message:
    :param new_msg:
    :return: None
    """
    if not data.globals.users_dict[message.from_user.id]["message_id"] == 0:
        bot.edit_message_reply_markup(
            message.chat.id,
            message_id=data.globals.users_dict[message.from_user.id]["message_id"],
            reply_markup="",
        )
    data.globals.users_dict[message.from_user.id]["message_id"] = new_msg.message_id


def delete_msg(chat_id: int, user_id: int) -> None:
    """
    Function. Delete message.
    :param chat_id:
    :param user_id:
    :return: None
    """
    if not data.globals.users_dict[user_id]["message_id"] == 0:
        bot.delete_message(chat_id, data.globals.users_dict[user_id]["message_id"])

    if data.globals.users_dict[user_id]["message_list"]:
        for msg in data.globals.users_dict[user_id]["message_list"]:
            bot.delete_message(chat_id, msg)
        data.globals.users_dict[user_id]["message_list"].clear()


def edit_reply_msg(chat_id: int, user_id: int) -> None:
    """
    Function. Edit inline kb.
    :param chat_id:
    :param user_id:
    :return: None
    """
    if not data.globals.users_dict[user_id]["message_id"] == 0:
        bot.edit_message_reply_markup(
            chat_id, data.globals.users_dict[user_id]["message_id"], reply_markup=""
        )
