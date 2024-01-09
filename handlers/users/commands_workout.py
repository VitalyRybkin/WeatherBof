from random import choice

from handlers.users import set_location, help
from loader import bot
from utils.reply_center import Reply
import data.globals as global_var


@bot.message_handler(content_types=["text"])
def typed_commands(message):

    reply_user_from = Reply(message)
    if message.text.lower().strip() == "start":
        global_var.count_not_defined_typings = 0
        bot.send_message(
            message.chat.id,
            "I'm already running, but anyway...\n" "Here's some help for you:",
        )
        help.help_message(message)
    elif message.text.lower().strip() == "help":
        global_var.count_not_defined_typings = 0
        help.help_message(message)
    elif message.text.lower().strip() == "set":
        global_var.count_not_defined_typings = 0
        set_location.search_location(message)
    elif (
        message.text.lower().strip() in ["hi", "hello"]
        or "hi" in message.text.lower().strip()
    ):
        reply_user_from = Reply(message)
        hello = choice(reply_user_from.hellos)
        addressee = choice(reply_user_from.addressees)
        bot.send_message(
            message.chat.id,
            f"{hello}, "
            f"{addressee}"
            f'{"?!" if "How " in hello or "What" in hello else "!"}',
        )
    else:
        if global_var.count_not_defined_typings > 1:
            bot.send_message(
                message.chat.id,
                f"{message.from_user.first_name}, " f"{choice(reply_user_from.tired)}",
            )
            global_var.count_not_defined_typings = 0
        else:
            global_var.count_not_defined_typings += 1
            bot.send_message(message.chat.id, choice(reply_user_from.not_defined))
