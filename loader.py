from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from data import config

bot = TeleBot(token=config.BOT_TOKEN, state_storage=StateMemoryStorage())
