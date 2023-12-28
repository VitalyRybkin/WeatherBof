from random import choice

from handlers.default import help
from handlers.users import set_city
from loader import bot
from utils.reply_center import Reply


@bot.message_handler(content_types=["text"])
def typed_commands(message):
    global count_not_defines

    reply_user_from = Reply(message)
    if message.text.lower().strip() == "start":
        count_not_defines = 0
        bot.send_message(
            message.chat.id,
            "I'm already running, but anyway...\n" "Here's some help for you:",
        )
        help.help_message(message)
    elif message.text.lower().strip() == "help":
        count_not_defines = 0
        help.help_message(message)
    elif message.text.lower().strip() == "set":
        count_not_defines = 0
        set_city.search_location(message)
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
        if count_not_defines > 1:
            bot.send_message(
                message.chat.id,
                f"{message.from_user.first_name}, " f"{choice(reply_user_from.tired)}",
            )
            count_not_defines = 0
        else:
            count_not_defines += 1
            bot.send_message(message.chat.id, choice(reply_user_from.not_defined))
