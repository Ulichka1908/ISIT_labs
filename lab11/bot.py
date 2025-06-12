import telebot
from telebot import types, apihelper
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import xml.dom.minidom  # Не забудь импортировать!

# Кастомный адаптер, отключающий проверку SSL
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl._create_unverified_context()
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# Переопределение сессии у apihelper
session = requests.Session()
session.mount("https://", SSLAdapter())
apihelper.session = session

bot = telebot.TeleBot('7728709478:AAH4qCRtvBoGJPpfPUtMyBbxsUMiCoSKs5A')

selected_currency = {}

# === Команда /start ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("USD")
    btn2 = types.KeyboardButton("EUR")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=markup)

# === Обработка выбора валюты ===
@bot.message_handler(func=lambda message: message.text in ['USD', 'EUR'])
def currency_chosen(message):
    chat_id = message.chat.id
    selected_currency[chat_id] = message.text
    bot.send_message(chat_id, f"Вы выбрали {message.text}. Введите дату в формате ДД.ММ.ГГГГ")

# === Обработка ввода даты ===
@bot.message_handler(func=lambda message: True)
def get_currency_rate(message):
    chat_id = message.chat.id
    if chat_id not in selected_currency:
        bot.send_message(chat_id, "Пожалуйста, сначала выберите валюту с помощью /start")
        return

    date = message.text.strip()
    currency_code = selected_currency[chat_id]

    try:
        url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
        r = apihelper.session.get(url)  # Используем кастомную сессию
        dom = xml.dom.minidom.parseString(r.text)
        dom.normalize()

        currencies = dom.getElementsByTagName("Valute")
        for currency in currencies:
            char_code = currency.getElementsByTagName("CharCode")[0].childNodes[0].nodeValue
            if char_code == currency_code:
                value = currency.getElementsByTagName("Value")[0].childNodes[0].nodeValue
                bot.send_message(chat_id, f"Курс {currency_code} на {date} составляет {value} руб.")
                return

        bot.send_message(chat_id, f"Не удалось найти курс валюты {currency_code} на дату {date}")

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при получении данных: {e}")

# === Запуск бота ===
bot.polling(none_stop=True)
