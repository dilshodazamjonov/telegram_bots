from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def bot_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)  # Область для кнопок
    btn1 = KeyboardButton(text='🌎 CountryInfo')  # Создали кнопку
    btn2 = KeyboardButton(text='☁ Weather')  # Создали кнопку

    markup.add(btn1, btn2)  # Добавили кнопки в область
    return markup  # Функция вернёт готовую область с кнопками