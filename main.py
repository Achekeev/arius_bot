import datetime
import telebot
from telebot import types

bot = telebot.TeleBot('5574488884:AAGyzUCthZs-fcDpX-yaczVk8x18KdiHBGE')


@bot.message_handler(commands=['start'])
def url(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_my_site = types.InlineKeyboardButton('Наш Сайт', callback_data='Наш Сайт',url='https://www.google.com')
    btn_main_house = types.InlineKeyboardButton('Виды', callback_data='Виды')
    btn_plans = types.InlineKeyboardButton('Планировка', callback_data='Планировка')
    btn_history = types.InlineKeyboardButton('Наша История', callback_data='Наша История')
    btn_prices = types.InlineKeyboardButton('Наши Цены', callback_data='Наши Цены')
    markup.add(btn_my_site, btn_main_house, btn_plans, btn_history, btn_prices)
    bot.send_message(message.chat.id, 'Press Button', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_main_house(call):
    if call.data == 'Виды':
        pic = open("images/1_View01.jpg", 'rb')
        bot.send_photo(call.message.chat.id, pic)
    elif call.data == 'Планировка':
        pic1 = open("images/1_plan.jpg", 'rb')
        pic2 = open("images/2_plan.jpg", 'rb')
        pic3 = open("images/3_plan.jpg", 'rb')
        pic4 = open("images/4_plan.jpg", 'rb')
        bot.send_document(call.message.chat.id, pic1)
        bot.send_document(call.message.chat.id, pic2)
        bot.send_document(call.message.chat.id, pic3)
        bot.send_document(call.message.chat.id, pic4)
    elif call.data == 'Наша История':
        history_mess = 'Text Message'
        bot.send_message(call.message.chat.id, history_mess)
    elif call.data == 'Наши Цены':
        bot.send_message(call.message.chat.id, 'Prices List')


bot.polling()
