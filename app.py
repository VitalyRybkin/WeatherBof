import atexit
import copy
import json
# import pickle
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
bot.register_message_handler(handlers.users.preferences)
bot.register_message_handler(handlers.users.wishlist)
bot.register_message_handler(handlers.users.user_config)
bot.register_message_handler(handlers.call_backs.user_config_callback)
bot.register_message_handler(handlers.call_backs.default_callback)
bot.register_message_handler(handlers.call_backs.add_location_callback)
bot.register_message_handler(handlers.call_backs.wishlist_callback)
bot.register_message_handler(handlers.call_backs.settings_callback)
bot.register_message_handler(handlers.users.commands_workout)


if __name__ == "__main__":
    print("Bot has started!")
    admin_notify()
    set_menu_commands(bot)

    DATABASE = config.DB


    def handler(signum, frame):
        # with open('./data/settings.pkl', 'wb') as file:
        #     print("Signal Number:", signum, " Frame: ", frame)
        #     pickle.dump(data.globals.users_dict, file)
        with open("./data/user_dict.json", "w") as write_dict:
            json.dump(data.globals.users_dict, write_dict, indent=4)
            print("Signal Number:", signum, " Frame: ", frame)


    atexit.register(handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    if os.path.exists('./data/user_dict.json'):
        # with open('settings.pkl', 'rb') as f:
        #     data.globals.users_dict = pickle.load(f)
        with open("./data/user_dict.json", "r") as read_dict:
            json_dict = json.load(read_dict)
        new_dict = {}
        for k, v in json_dict.items():
            new_dict[int(k)] = v
            if v['state'] is None and not v['message_id'] == 0:
                print(v['chat_id'], v['message_id'])
                bot.delete_message(v['chat_id'], v['message_id'])
                v['message_id'] = 0
            bot.set_state(v['user_id'], v['state'], v['chat_id'])
        data.globals.users_dict = copy.deepcopy(new_dict)

    if not os.path.exists(f'./data/{DATABASE}'):
        with sqlite3.connect(f'./data/{DATABASE}') as connection:
            cursor = connection.cursor()
            cursor.executescript(open("./data/schema.sql", "r").read())
            connection.commit()
            cursor.close()

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
