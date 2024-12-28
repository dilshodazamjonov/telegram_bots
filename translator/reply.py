from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs import LANGUAGES

def button_dest(src):
    mark_up = InlineKeyboardMarkup()

    buttons = []
    for key, value in LANGUAGES.items():
        btn = InlineKeyboardButton(text = value, callback_data=f'dest_{src}_{key}')
        buttons.append(btn)

    mark_up.add(*buttons)
    return mark_up


def button_src():
    mark_up = InlineKeyboardMarkup()

    buttons = []
    for key, value in LANGUAGES.items():
        btn = InlineKeyboardButton(text=value, callback_data=f'src_{key}')
        buttons.append(btn)

    mark_up.add(*buttons)
    return mark_up


