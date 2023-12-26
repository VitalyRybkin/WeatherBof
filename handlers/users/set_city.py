from keyboards.reply.reply_buttons import reply_cancel_button
from loader import bot
from states.bot_states import States
from utils.signs_text import ButtonSigns


@bot.message_handler(commands=["set"])
@bot.message_handler(state=States.set_city)
def set_city(message):
    """
    Function. Setting users favorite city.
    :return:
    """
    if bot.get_state(message.from_user.id, message.chat.id) is None:
        bot.set_state(message.from_user.id, States.set_city, message.chat.id)
    # print('set city')
    # print(bot.current_states.get_state(message.chat.id, message.from_user.id))
    if message.text == ButtonSigns.cancel:
        bot.delete_state(message.from_user.id, message.chat.id)
        return
    cancel_button = reply_cancel_button()
    bot.send_message(message.chat.id, "Type in city name:", reply_markup=cancel_button)
    pass
