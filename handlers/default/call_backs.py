from loader import bot
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Cancel":
        bot.delete_state(call.message.from_user.id, call.message.chat.id)
        bot.send_message(call.message.chat.id, "Cancelled!")
