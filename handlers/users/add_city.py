from loader import bot
from states.bot_states import States


@bot.message_handler(commands=["add"])
@bot.message_handler(state=States.add_city)
def add_city():
    pass
