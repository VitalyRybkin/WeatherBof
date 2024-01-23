from telebot.handler_backends import StatesGroup, State


class States(StatesGroup):
    start = State()  # +
    set_location = State()  # +
    add_location = State()  # +
    search_location = State()  # +
    change_wishlist = State()  # +
    empty_wishlist = State()  # +
    wishlist = State()  # +
    my_prompt = State()  # +
    customize_prompt = State()  # +
    customize_current = State()  # +
    customize_hourly = State()  # +
    customize_daily = State()  # +
    change_setting = State()  # +
    user_config_prompt = State()  # +
    config_settings = State()  # +
    default_config_prompt = State()
    default_setting = State()
    set_duration_prompt = State()
    weather_display_hourly = State()  # +
    weather_display_daily = State()  # +
