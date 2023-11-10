from loader import bot


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!\n'
                                      f'Welcome to the club!\n\n'
                                      f'From now on, I\'m your weather forecast partner!\n'
                                      f'Look what I can do for you!')
