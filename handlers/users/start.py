# from keyboards.reply.reply_buttons import add_button
from keyboards.inline.inline_buttons import show_weather, add_button
from loader import bot
from midwares.db_conn_center import read_data, write_data
from midwares.sql_lib import Users, Favorites
from states.bot_states import States
from utils.reply_center import Reply


@bot.message_handler(commands=["start"])
@bot.message_handler(state=States.start)
def start_command(message):
    bot.set_state(message.from_user.id, States.start, message.chat.id)
    query = f'SELECT {Users.user_id} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id}'
    get_user_info = read_data(query)
    if not get_user_info:
        write_data(f'INSERT INTO {Users.table_name} ("{Users.user_id}") VALUES ({message.from_user.id})')
        bot.send_message(
            message.chat.id,
            f"Hello, {message.from_user.first_name}!\n"
            f"Welcome to our weather forecasting community!\n\n"
            f"From now on, I'm your weather forecasting partner!\n"
            f"Look, what I can do for you:",
        )
        reply_from = Reply(message)
        res = '\n'.join('{} - {}'.format(k, v) for k, v in reply_from.help.items())
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!\n"
                                          f"Welcome back!")
        if len(get_user_info[0]) == 1:
            add_city_keyboard = add_button()
            bot.send_message(message.chat.id, 'You haven\'t set your favorite city, yet!', reply_markup=add_city_keyboard)
            # user_text = message.text
            # if user_text == 'Cancel':
            #     bot.delete_state(message.from_user.id, message.chat.id)
            # else:
            #     # TODO State.add
            #     pass
            #     # bot.set_state(message.from_user.id, States.add_city, message.chat.id)
        else:
            # TODO State.cancel
            check_weather_keyboard = show_weather()
            bot.send_message(message.chat.id, f'Your favorite city: {get_user_info[0][1]}', reply_markup=check_weather_keyboard)


