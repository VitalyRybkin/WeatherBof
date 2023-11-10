from loader import bot
from utils.reply_center import Reply


@bot.message_handler(commands=['help'])
def help_message(message):
    reply_from = Reply(message)
    res = '\n'.join('{} - {}'.format(k, v) for k, v in reply_from.help.items())
    bot.send_message(message.chat.id, res)
