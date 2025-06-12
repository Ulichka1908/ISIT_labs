# -*- coding: utf-8 -*-
import telebot
from telebot import types
import ssl
import requests
from telebot import TeleBot, apihelper

class UnsafeHTTPSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

unsafe_session = requests.Session()
unsafe_session.mount("https://", UnsafeHTTPSAdapter())

apihelper.session = unsafe_session

bot = TeleBot("7728709478:AAH4qCRtvBoGJPpfPUtMyBbxsUMiCoSKs5A")


clicks = {
    'Меню еды': 0,
    'Меню напитков': 0,
    'Статистика': 0,
    'Супы': 0,
    'Горячее': 0,
    'Чай': 0,
    'Кофе': 0
}

def main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🍽 Меню еды', '🥤 Меню напитков', '📊 Статистика')
    bot.send_message(chat_id, 'Выберите раздел:', reply_markup=keyboard)

def food_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🥣 Супы', '🍝 Горячее', '🔙 Назад')
    bot.send_message(chat_id, 'Выберите категорию еды:', reply_markup=keyboard)

def drinks_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🍵 Чай', '☕ Кофе', '🔙 Назад')
    bot.send_message(chat_id, 'Выберите напиток:', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! 👋')
    main_menu(message.chat.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text

    if text == '🍽 Меню еды':
        clicks['Меню еды'] += 1
        food_menu(message.chat.id)

    elif text == '🥤 Меню напитков':
        clicks['Меню напитков'] += 1
        drinks_menu(message.chat.id)

    elif text == '📊 Статистика':
        clicks['Статистика'] += 1
        stats = "\n".join([f"{key}: {value}" for key, value in clicks.items()])
        bot.send_message(message.chat.id, f"📈 Статистика нажатий:\n{stats}")

    elif text == '🥣 Супы':
        clicks['Супы'] += 1
        bot.send_message(message.chat.id, 'Вы выбрали суп 🍲')

    elif text == '🍝 Горячее':
        clicks['Горячее'] += 1
        bot.send_message(message.chat.id, 'Вы выбрали горячее блюдо 🔥')

    elif text == '🍵 Чай':
        clicks['Чай'] += 1
        bot.send_message(message.chat.id, 'Вы выбрали чай 🍵')

    elif text == '☕ Кофе':
        clicks['Кофе'] += 1
        bot.send_message(message.chat.id, 'Вы выбрали кофе ☕')

    elif text == '🔙 Назад':
        main_menu(message.chat.id)

    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите пункт из меню.')

bot.polling(none_stop=True)
