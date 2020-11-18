# -*- coding: utf-8 -*-
import config
import telebot
import sys
from telebot import types
import subprocess

bot = telebot.TeleBot(config.token)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока', '/ip', '/camera')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_team = types.InlineKeyboardButton(text='TeamViewer', callback_data='teamViewer')
    btn_kill_team = types.InlineKeyboardButton(text='Выключить TeamViewer', callback_data='kill_team')
    btn_help = types.InlineKeyboardButton(text='Помощь', callback_data='help')
    markup.add(btn_team, btn_kill_team)
    markup.add(btn_help)
    bot.send_message(message.chat.id, 'Привет! Я Bot srv_home!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if config.user_id == call.message.chat.id:
        if call.data == 'teamViewer':
            cmd = '/usr/bin/teamviewer > /dev/null 2>&1 &'
            subprocess.Popen(cmd, shell=True)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Я Bot выполнил вашу просьбу и запустил TeamViewer")
        elif call.data == 'kill_team':
            subprocess.call("killall TeamViewer &", shell=True)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Привет! Я могу Вам помочь?')
        elif call.data == 'help':
            bot.send_message(call.message.chat.id, 'Привет! Я могу помочь! Вот список команд /start')
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="У Вас нет прав доступа")


@bot.message_handler(commands=['help'])
def send_command(message):
    bot.send_message(message.chat.id, 'Привет! Я могу запустить другую команду!')


@bot.message_handler(commands=['reply'])
def reply_message(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['url'])
def reply_url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Наш сайт', url='http://vip-dw.org')
    markup.add(btn_my_site, btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
