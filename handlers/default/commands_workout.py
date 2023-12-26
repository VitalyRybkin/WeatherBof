from random import choice

from handlers.default import help
from keyboards.reply.reply_buttons import reply_cancel_button
from loader import bot
from states.bot_states import States
from utils.reply_center import Reply
from data.globals import COUNT_NOT_DEFINED_TYPINGS as count_not_defines


@bot.message_handler(func=lambda message: message.text == "\U0001F3E1 Set city")
def setting_city(message):
    cancel_button = reply_cancel_button()
    bot.send_message(message.chat.id, "Type in city name:", reply_markup=cancel_button)
    bot.set_state(message.from_user.id, States.set_city, message.chat.id)


@bot.message_handler(func=lambda message: message.text == "\U0000274C Cancel")
def cancelling_state(message):
    print(bot.current_states.get_state(message.chat.id, message.from_user.id))
    bot.delete_state(message.from_user.id, message.chat.id)
    print('cancelled')


@bot.message_handler(content_types=["text"])
def typed_commands(message):
    global count_not_defines

    reply_from = Reply(message)
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
