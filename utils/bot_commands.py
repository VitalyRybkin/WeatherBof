from telebot.types import BotCommand


def set_menu_commands(bot):
    bot.set_my_commands(
        [
            # BotCommand(command="start", description="start weather forecasting"),
            BotCommand(command="my", description="your favorite location weather"),
            BotCommand(command="onetouch", description="favorite location weather by default"),
            BotCommand(command="default", description="default settings for 'onetouch'"),
            BotCommand(command="set", description="set/reset your favorite location"),
            BotCommand(command="wishlist", description="wishlist output"),
            BotCommand(command="change", description="change your wishlist"),
            BotCommand(command="add", description="add location to a wishlist"),
            BotCommand(command="empty", description="clear your wishlist"),
            BotCommand(command="prefs", description="change your display settings"),
            BotCommand(command="userconfig", description="user settings (units and more)"),
            BotCommand(command="help", description="start helping you"),
        ]
    )
