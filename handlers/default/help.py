from loader import bot
from utils.reply_center import Reply


@bot.message_handler(commands=['help'])
def help_message(message):
    reply_from = Reply(message)
    res = '\n'.join('{} - {}'.format(k, v) for k, v in reply_from.help.items())
    # res = '\n'.join(f'{k:<15} - {v}' for k, v in reply_from.help.items())
    bot.send_message(message.chat.id, res)
    if bot.get_state(message.from_user.id, message.chat.id):
        bot.delete_state(message.from_user.id, message.chat.id)
