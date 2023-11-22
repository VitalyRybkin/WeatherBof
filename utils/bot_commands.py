from telebot.types import BotCommand


def set_menu_commands(bot):
    bot.set_my_commands(
        [
            # BotCommand(command="start", description="start weather forecasting"),
            BotCommand(command="my", description="your city weather forecast"),
            BotCommand(command="del", description="delete your city"),
            BotCommand(command="change", description="change your city"),
            BotCommand(command="wishlist", description="wishlist output"),
            BotCommand(command="add", description="add place to a wish list"),
            BotCommand(command="empty", description="clear your wishlist"),
            BotCommand(command="remove", description="remove city from your wishlist"),
            BotCommand(command="help", description="start helping me"),
        ]
    )
