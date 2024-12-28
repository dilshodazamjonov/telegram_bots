from telebot.types import Message, CallbackQuery
from telebot import TeleBot
from googletrans import Translator
from configs import *
from reply import button_dest, button_src
import psycopg2
from psycopg2 import sql, extras #(Чтобы легко взять инфо из ДБ ввиде словаря)
from contextlib import contextmanager #(чтобы работать с БД и файлами)

bot = TeleBot('') # your IP token that you take after creating the bot via Fatherbot in telegram=


# I used postgresql so for the fields something will be different for you
#Creating Table
@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname='hw_telegram', #here put the name of the database name that you created for this project
        host='localhost',
        port='5432',
        user='postgres',
        password='12345678' # here you have to put your password to access to pgadmin4
    )
    try:
        yield conn
    finally:
        conn.close()

def create_translations_history():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translation_history(
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL,
            original_text TEXT NOT NULL,
            src_lang VARCHAR(10) NOT NULL,
            dest_lang VARCHAR(10) NOT NULL,
            translated_text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
        ''')
        conn.commit()
        cursor.close()

create_translations_history()

#Saving_info_to_database
def save_translation(user_id, original_text, src_lang, dest_lang, translated_text):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            insert_query = sql.SQL("""
                INSERT INTO translation_history (user_id, original_text, src_lang, dest_lang, translated_text)
                VALUES (%s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (user_id, original_text, src_lang, dest_lang, translated_text))
            conn.commit()
            cursor.close()
    except psycopg2.Error as e:
        print(f"Error saving translation: {e}")

# Retrieving data from DB

def get_translation_history(user_id):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            select_query = sql.SQL("""
                SELECT original_text, src_lang, dest_lang, translated_text, timestamp
                FROM translation_history
                WHERE user_id = %s
                ORDER BY timestamp DESC
            """)
            cur.execute(select_query, (user_id,))
            history_entries = cur.fetchall()
            cur.close()
            return history_entries
    except psycopg2.Error as e:
        print(f"Error fetching translation history: {e}")
        return []

# Starting for the bots
@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def commands_for_bot(message: Message):
    chat_id = message.chat.id
    username = message.from_user.username
    if message.text == '/start':
        msg = f'Hello {username}, bot-translator welcomes you'
        bot.send_message(chat_id, msg)
        confirm_dest_asc_src(message)

    elif message.text == '/help':
        msg = f'By help you can contact to the owner @d_azamjonov'
        bot.send_message(chat_id, msg)

    elif message.text == '/about':
        msg = f'This bot can help to translate one word from Russian to a language you choose'
        bot.send_message(chat_id, msg)

    elif message.text == '/history':
        history_entries = get_translation_history(message.from_user.id)
        if not history_entries:
            bot.send_message(chat_id, 'No translation history yet.')
        else:
            msg = 'Translation History:\n\n'
            for entry in history_entries:
                msg += f'From {LANGUAGES[entry["src_lang"]]} to {LANGUAGES[entry["dest_lang"]]}:\n'
                msg += f'Original text: {entry["original_text"]}\n'
                msg += f'After translation: {entry["translated_text"]}\n'
                msg += f'Time: {entry["timestamp"]}\n\n'
            bot.send_message(chat_id, msg)

def confirm_dest_asc_src(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Choose from which language do you want to translate: ', reply_markup=button_src())

@bot.callback_query_handler(func=lambda call: 'src' in call.data)
def confirm_call(call: CallbackQuery):
    _, text_src = call.data.split('_')
    chat_id = call.message.chat.id

    bot.send_message(chat_id, 'Enter a language to translate to: ', reply_markup=button_dest(text_src))

@bot.callback_query_handler(lambda call: 'dest' in call.data)
def confirm_dest_src_asc(call: CallbackQuery):
    _, text_src, text_dest = call.data.split('_')
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Enter text to translate')
    bot.register_next_step_handler(call.message, get_text_for_translate, text_src, text_dest)

def get_text_for_translate(message: Message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id

    if text.startswith('/'):
        commands_for_bot(message)
    else:
        translator = Translator()
        result = translator.translate(text=text, src=text_src, dest=text_dest).text

        # Save translation to database
        save_translation(user_id, text, text_src, text_dest, result)

        # Send translated result to user
        bot.send_message(chat_id, result)
        msg = f'Translation from {LANGUAGES[text_src]} to {LANGUAGES[text_dest]} saved to history. Enter new text or command.'
        bot.send_message(chat_id, msg)
        bot.register_next_step_handler(message, get_text_for_translate, text_src, text_dest)

bot.infinity_polling()
