from telebot.types import BotCommand


def set_menu_commands(bot):
    bot.set_my_commands(
        [
            # BotCommand(command="start", description="start weather forecasting"),
            BotCommand(command="my", description="your favorite location weather"),
            BotCommand(command="set", description="set/reset favorite your location"),
            BotCommand(command="del", description="delete your favorite location"),
            BotCommand(command="wishlist", description="wishlist output"),
            BotCommand(command="change", description="change your wishlist"),
            BotCommand(command="add", description="add location to a wishlist"),
            BotCommand(command="empty", description="clear your wishlist"),
            BotCommand(command="preferences", description="your default settings"),
            BotCommand(command="help", description="start helping me"),
        ]
    )
