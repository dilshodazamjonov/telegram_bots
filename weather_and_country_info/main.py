from math import lgamma
from telebot import TeleBot
from telebot.types import Message
from weather_data import *
from buttons import *
from country_data import *

TOKEN = ''

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    chat_id2 = message.from_user.id
    username = message.from_user.first_name
    bot.reply_to(message, f'Hello {username}, I am ready to help you with retrieving weather data!')
    bot.send_message(chat_id, 'To continue further send me your contact details by clicking the button below',
                     reply_markup=bot_buttons())

def get_weather_text(message: Message):
    chat_id = message.chat.id
    country_name = message.text
    result =get_weather_country(country_name)
    bot.send_message(chat_id, result)

@bot.message_handler(regexp='☁ Weather')
def reaction_for_weather(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Enter the valid country name to get the current weather data: ')
    bot.register_next_step_handler(message, get_weather_text)

def get_country_text(message: Message):
    chat_id = message.chat.id
    country_name = message.text
    result =get_country_info(country_name)
    bot.send_message(chat_id, result)

@bot.message_handler(regexp='🌎 CountryInfo')
def reaction_for_country(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Enter the name of the country you would like to know about: ')
    bot.register_next_step_handler(message, get_country_text)

bot.polling(none_stop=True)