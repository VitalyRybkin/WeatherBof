from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Add_city":
        bot.answer_callback_query(call.id, "Add_city")
    elif call.data == "button2":
        bot.answer_callback_query(call.id, "Вы выбрали кнопку 2")
    elif call.data == "button3":
        bot.answer_callback_query(call.id, "Вы выбрали кнопку 3")
    elif call.data == "button4":
        bot.answer_callback_query(call.id, "Вы выбрали кнопку 4")
