from keyboards.inline.inline_buttons import inline_add_button
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Favorites


@bot.message_handler(commands=["wishlist"])
def wishlist_command(message):
    query = f'SELECT {Favorites.user_favorite_city_name} FROM {Favorites.table_name} WHERE {Favorites.favorites_user_id}={message.from_user.id}'
    get_favorite_city = read_data(query)
    add_city_menu = inline_add_button()
    if not get_favorite_city:
        bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)
