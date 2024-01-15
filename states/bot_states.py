from telebot.handler_backends import StatesGroup, State


class States(StatesGroup):
    start = State()
    add_location = State()
    search_location = State()
    help = State()
    cancel = State()
    change_wishlist = State()
    empty_wishlist = State()
    wishlist = State()
    set_location = State()
    my = State()
    customize_prompt = State()
    customize_current = State()
    customize_hourly = State()
    customize_daily = State()
    change_setting = State()
    user_config_setting = State()
    config_settings = State()
    default_config_prompt = State()
    default_setting = State()
    set_duration_prompt = State()
