from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_add_location_prompt_btn
from loader import bot
from states.bot_states import States


@bot.message_handler(commands=["add"])
@bot.message_handler(state=States.add_location)
def add_wishlist_location(message):
    markup = types.InlineKeyboardMarkup()
    add_location_keyboard = markup.row(inline_add_location_prompt_btn(), inline_cancel_btn())
    msg = bot.send_message(
        message.chat.id, "Add location to your wishlist?", reply_markup=add_location_keyboard
    )
    data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id
