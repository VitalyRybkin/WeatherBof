from keyboards.reply.reply_buttons import reply_cancel_button
from loader import bot
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Cancel":
        bot.delete_state(call.message.from_user.id, call.message.chat.id)
        bot.send_message(call.message.chat.id, "\U0000274C Cancel!")
    # if call.data == "Add city":
    #     bot.set_state(call.message.from_user.id, States.add_city, call.message.chat.id)
    #     cancel_button = reply_cancel_button()
    #     bot.send_message(
    #         call.message.chat.id, "Type in city name:", reply_markup=cancel_button
    #     )
