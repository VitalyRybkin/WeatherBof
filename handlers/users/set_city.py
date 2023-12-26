from keyboards.reply.reply_buttons import reply_cancel_button
from loader import bot
from states.bot_states import States


@bot.message_handler(commands=["set"])
@bot.message_handler(state=States.set_city)
def set_city(message):
    """
    Function. Setting users favorite city.
    :return:
    """
    cancel_button = reply_cancel_button()
    bot.send_message(message.chat.id, "Type in city name:", reply_markup=cancel_button)
    print('set city')
    pass
