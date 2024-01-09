from loader import bot


@bot.message_handler(commands=["customize"])
def custom(message):
    print(message.chat.id)
