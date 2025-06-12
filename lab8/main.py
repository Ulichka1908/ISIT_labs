import telebot
from telebot import types

TOKEN = '7728709478:AAH4qCRtvBoGJPpfPUtMyBbxsUMiCoSKs5A'
bot = telebot.TeleBot(TOKEN)

click_counter = {}

def update_counter(button_name):
    if button_name in click_counter:
        click_counter[button_name] += 1
    else:
        click_counter[button_name] = 1


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Меню еды', 'Меню напитков']
    keyboard.add(*[types.KeyboardButton(name) for name in buttons])
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Меню еды':
        update_counter('Меню еды')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Супы', 'Горячее', 'Назад']
        keyboard.add(*[types.KeyboardButton(name) for name in buttons])
        bot.send_message(message.chat.id, 'Выберите раздел еды:', reply_markup=keyboard)

    elif message.text == 'Меню напитков':
        update_counter('Меню напитков')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Чай', 'Кофе', 'Назад']
        keyboard.add(*[types.KeyboardButton(name) for name in buttons])
        bot.send_message(message.chat.id, 'Выберите раздел напитков:', reply_markup=keyboard)

    elif message.text in ['Супы', 'Горячее', 'Чай', 'Кофе']:
        update_counter(message.text)
        bot.send_message(message.chat.id, f'Вы выбрали {message.text}.')

    elif message.text == 'Назад':
        start(message)

    elif message.text == 'Статистика':
        stats = "\n".join([f"{key}: {value}" for key, value in click_counter.items()])
        bot.send_message(message.chat.id, f'Статистика нажатий:\n{stats}')

    else:
        bot.send_message(message.chat.id, 'Я не понимаю эту команду.')


bot.polling(none_stop=True)
