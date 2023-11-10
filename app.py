from loader import bot
import handlers
from utils.notifications import admin_notify
from utils.bot_commands import set_menu_commands

bot.register_message_handler(handlers.users.start)
bot.register_message_handler(handlers.default.help)
bot.register_message_handler(handlers.default.commands_workout)

if __name__ == '__main__':
    print('Bot has started!')
    admin_notify()
    set_menu_commands(bot)
    bot.infinity_polling()
