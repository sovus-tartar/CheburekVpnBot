import telebot
import os, sys
import subprocess
from telebot import types

chat_id = "chat_id"
token = "token"

bot = telebot.TeleBot(chat_id + ':' + token)

name_hashmap = {}
mode_hashmap = {}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if not message.from_user.id in mode_hashmap:
		mode_hashmap[message.from_user.id] = 0
		name_hashmap[message.from_user.id] = []

	mode = mode_hashmap[message.from_user.id]
	if mode == 0:
		if message.text == "Получить ключ":
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			btn = types.KeyboardButton("Отмена")
			markup.add(btn)
			mode_hashmap[message.from_user.id] = 1
			bot.send_message(message.from_user.id, "Для получения ключа, введите название для него латиницей", reply_markup=markup)
		elif message.text == "Связаться с автором":
			bot.send_message(message.from_user.id, "@sovus_tartar")
		else:
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			btn1 = types.KeyboardButton("Получить ключ")
			btn2 = types.KeyboardButton("Связаться с автором")
			markup.add(btn1, btn2)
			bot.send_message(message.from_user.id, "Здравствуйте! Чего изволите?", reply_markup=markup)

	if mode == 1:
		if message.text == "Отмена":
			mode_hashmap[message.from_user.id] = 0
			get_text_messages(message)
		else:
			name_hashmap[message.from_user.id].append(message.text)
			name = message.text

			str = "Вы хотите создать ключ с названием " + name + "?"
			btn1 = types.KeyboardButton("Да")
			btn2 = types.KeyboardButton("Нет")
			mode_hashmap[message.from_user.id] = 2
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			markup.add(btn1, btn2)

			bot.send_message(message.from_user.id, str, reply_markup=markup)
	if mode == 2:
		if message.text == "Да":
			markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
			name = name_hashmap[message.from_user.id][-1]
			bot.send_message(message.from_user.id, "Идёт создание ключа")
			get_key(name)
			bot.send_message(message.from_user.id, "Ключ создан. Для использование необходимо его скачать и поделиться им в приложение OpenVpn", reply_markup=markup)
			f = open("./ovpn_keys/"+name+".ovpn","rb")
			bot.send_document(message.chat.id, f)
			f.close()
			mode_hashmap[message.from_user.id] = 0
		else:
			mode_hashmap[message.from_user.id] = 0
			markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
			bot.send_message(message.from_user.id, "Отменяем...", reply_markup=markup)

def get_key(clientName : str):
	subprocess.call(['bash',  './new_client.sh', clientName])

def send_key(clientName: str, user_id):
	subprocess.call(['bash',  './send_key.sh', str(user_id), token, clientName])


bot.polling(none_stop=True, interval=3)

