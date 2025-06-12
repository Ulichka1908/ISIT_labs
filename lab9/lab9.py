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

likes = 0
dislikes = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    like_btn = types.InlineKeyboardButton(text=f"👍 Нравится ({likes})", callback_data="like")
    dislike_btn = types.InlineKeyboardButton(text=f"👎 Не нравится ({dislikes})", callback_data="dislike")
    keyboard.add(like_btn, dislike_btn)

    bot.send_message(message.chat.id, "Что ты думаешь об этом боте?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['like', 'dislike'])
def callback_handler(call):
    global likes, dislikes

    if call.data == 'like':
        likes += 1
    elif call.data == 'dislike':
        dislikes += 1

    keyboard = types.InlineKeyboardMarkup()
    like_btn = types.InlineKeyboardButton(text=f"👍 Нравится ({likes})", callback_data="like")
    dislike_btn = types.InlineKeyboardButton(text=f"👎 Не нравится ({dislikes})", callback_data="dislike")
    keyboard.add(like_btn, dislike_btn)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    bot.answer_callback_query(call.id, text="Спасибо за твой выбор!")

bot.polling(none_stop=True)
