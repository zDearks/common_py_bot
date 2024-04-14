import telebot
from telebot import types
import requests
import json
import random
from random import choice

bot = telebot.TeleBot('6869376581:AAF31echOpLwkK4UImCCr_OUk7I8tMxDmTc')




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я телеграм-бот. Отправьте /help для получения списка доступных мне команд")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Доступные команды:
    /start - начать работу с ботом
    /help - показать эту справку
    /giphy - получить случайный GIF
    /echo - повторить ваше сообщение
    /keyboard - показать клавиатуру
    /markup - показать inline-клавиатуру
    /remove - удалить клавиатуру
    /dice - бросить кубик
    """
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['giphy'])
def send_gif(message):
    url = "http://api.giphy.com/v1/gifs/random?api_key=X2WVp5aasm9TAknhJxb5G73KPFBMwIpO"
    response = requests.get(url)
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    bot.send_animation(chat_id=message.chat.id, animation=gif_url)


@bot.message_handler(commands=['echo'])
def echo_message(message):
    bot.reply_to(message, message.text)

@bot.message_handler(commands=['keyboard'])
def show_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Кнопка 1')
    btn2 = types.KeyboardButton('Кнопка 2')
    keyboard.add(btn1, btn2)
    bot.send_message(chat_id=message.chat.id, text="Выберите кнопку:", reply_markup=keyboard)


@bot.message_handler(commands=['markup'])
def show_markup(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Кнопка 1', callback_data='1')
    btn2 = types.InlineKeyboardButton('Кнопка 2', callback_data='2')
    markup.add(btn1, btn2)
    bot.send_message(chat_id=message.chat.id, text="Выберите кнопку:", reply_markup=markup)


@bot.message_handler(commands=['remove'])
def remove_keyboard(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id=message.chat.id, text="Клавиатура удалена", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == '1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали кнопку 1")
        elif call.data == '2':
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали кнопку 2")
@bot.message_handler(commands=['dice'])
def roll_dice(message):
    dice_roll = random.randint(1, 6)
    bot.reply_to(message, f"Выпало число: {dice_roll}")


bot.polling()


