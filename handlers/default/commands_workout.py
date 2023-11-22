from random import choice

from handlers.default import help
from loader import bot
from utils.reply_center import Reply
from data.globals import COUNT_NOT_DEFINED_TYPINGS as count_not_defines


@bot.message_handler(content_types=["text"])
def typed_commands(message):
    global count_not_defines

    reply_from = Reply(message)
    if message.text.lower().strip() == "start":
        count_not_defines = 0
        bot.send_message(message.chat.id, 'I\'m already running, but anyway...\n'
                         'Here\'s some help for you:')
        help.help_message(message)
    elif message.text.lower().strip() == "help":
        count_not_defines = 0
        help.help_message(message)
    elif (
        message.text.lower().strip() in ["hi", "hello"]
        or "hi" in message.text.lower().strip()
    ):
        reply_from = Reply(message)
        hello = choice(reply_from.hellos)
        addressee = choice(reply_from.addressees)
        bot.send_message(
            message.chat.id,
            f"{hello}, "
            f"{addressee}"
            f'{"?!" if "How " in hello or "What" in hello else "!"}',
        )
    else:
        if count_not_defines > 1:
            bot.send_message(
                message.chat.id,
                f"{message.from_user.first_name}, " f"{choice(reply_from.tired)}",
            )
            count_not_defines = 0
        else:
            count_not_defines += 1
            bot.send_message(message.chat.id, choice(reply_from.not_defined))

