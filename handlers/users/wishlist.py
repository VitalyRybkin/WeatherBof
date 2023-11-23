from wheel.macosx_libfile import read_data

from loader import bot


@bot.message_handler(commands=["wishlist"])
def wishlist_command(message):
    pass