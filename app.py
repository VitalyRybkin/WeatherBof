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
bot.register_message_handler(handlers.default.help)
bot.register_message_handler(handlers.users.wishlist)
bot.register_message_handler(handlers.users.set_location)
bot.register_message_handler(handlers.users.add_location)
bot.register_message_handler(handlers.default.call_backs)
bot.register_message_handler(handlers.default.commands_workout)


if __name__ == "__main__":
    print("Bot has started!")
    admin_notify()
    set_menu_commands(bot)

    DATABASE = config.DB


    def handler(signum, frame):
        with open('settings.pkl', 'wb') as file:
            print("Signal Number:", signum, " Frame: ", frame)
            pickle.dump(data.globals.users_dict, file)


    atexit.register(handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    if os.path.exists('settings.pkl'):
        with open('settings.pkl', 'rb') as f:
            data.globals.users_dict = pickle.load(f)

    if not os.path.exists(f'./{DATABASE}'):
        with sqlite3.connect(f'{DATABASE}') as connection:
            cursor = connection.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON""")
            key = cursor.execute("PRAGMA foreign_keys")
            connection.commit()

            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   user_id INTEGER PRIMARY KEY NOT NULL,
                                   user_city VARCHAR(50))''')
            connection.commit()

            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
                                  id INTEGER PRIMARY KEY,
                                  favorites_user_id INTEGER NOT NULL,
                                  user_favorite_city_name VARCHAR(50) NOT NULL,
                                  FOREIGN KEY (favorites_user_id) REFERENCES users(user_id) 
                                  ON DELETE CASCADE
                                  ON UPDATE CASCADE)''')
            connection.commit()

            cursor = connection.cursor()
            cursor.execute('CREATE INDEX IF NOT EXISTS favorites_id_index ON favorites(id)')
            connection.commit()

            cursor = connection.cursor()
            cursor.execute('CREATE INDEX IF NOT EXISTS users_user_id_index ON users (user_id)')
            connection.commit()

            cursor.close()

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
