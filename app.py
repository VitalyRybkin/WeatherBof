import atexit
import pickle
import signal
import sqlite3

from telebot import custom_filters

from loader import bot
import handlers
from utils.notifications import admin_notify
from utils.bot_commands import set_menu_commands
from data import config
import os
import data.globals

bot.register_message_handler(handlers.users.start)
bot.register_message_handler(handlers.users.my)
bot.register_message_handler(handlers.users.help)
bot.register_message_handler(handlers.users.set_location)
bot.register_message_handler(handlers.users.empty)
bot.register_message_handler(handlers.users.add_location)
bot.register_message_handler(handlers.users.change)
bot.register_message_handler(handlers.users.watch_custom)
bot.register_message_handler(handlers.users.custom)
bot.register_message_handler(handlers.users.wishlist)
bot.register_message_handler(handlers.users.call_backs)
bot.register_message_handler(handlers.users.commands_workout)


if __name__ == "__main__":
    print("Bot has started!")
    admin_notify()
    set_menu_commands(bot)

    DATABASE = config.DB


    def handler(signum, frame):
        with open('./data/settings.pkl', 'wb') as file:
            print("Signal Number:", signum, " Frame: ", frame)
            pickle.dump(data.globals.users_dict, file)


    atexit.register(handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    if os.path.exists('./data/settings.pkl'):
        with open('settings.pkl', 'rb') as f:
            data.globals.users_dict = pickle.load(f)

    if not os.path.exists(f'./data/{DATABASE}'):
        with sqlite3.connect(f'./data/{DATABASE}') as connection:
            cursor = connection.cursor()
            cursor.executescript(open("./data/schema.sql", "r").read())
            connection.commit()
            cursor.close()

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
