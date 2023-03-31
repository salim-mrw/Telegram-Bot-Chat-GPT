#! /usr/local/bin/python
# -*- coding: UTF-8 -*-

from decouple import config
import telebot
from telebot import types, util
import json
from datetime import datetime
import openai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


text_messages = {
	"get started": u"*{firstname}* your message \n\n.",
	"about": u"your message \n\n.",
	"leavegroup": u"your message \n\n.",
	"prv": u"your message \n\n."
	"no bot": u"your message \n\n."
}

BOT_TOKEN = config("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

GPT_TOKEN = config("GPT_TOKEN")
openai.api_key = GPT_TOKEN
# openai.Model.list()


def saveInfo(message):

	Id = str(message.from_user.id)
	firstname = str(message.from_user.first_name)
	lastname = str(message.from_user.last_name)
	username = str(message.from_user.username)
	messageu = str(message.text)
	now = datetime.now()
	date = str(now.date())
	time = str(now.strftime("%H:%M:%S"))

	with open("info.json", "r", encoding='utf8') as infoJsonData:
		data = json.load(infoJsonData)
	infoJsonData.close()

	with open("message.json", "r", encoding='utf8') as messageJsonData:
		data1 = json.load(messageJsonData)
	messageJsonData.close()

	user = data["users"]
	messageus = data1["message"]

	if str(Id) not in user:
		user[Id] = {"nummessage": 1}

	for index in user:
		if index == Id:
			user[Id]["nummessage"] += 1

	if str(messageu) not in messageus:
		messageus[messageu] = {"allnummessage": 0}

	for index in messageus:
		if index == messageu:
			messageus[messageu]["allnummessage"] += 1

	user[Id]["name"] = firstname + " " + lastname
	user[Id]["username"] = username
	user[Id]["id"] = Id
	user[Id]["time"] = time
	user[Id]["date"] = date
	messageus[messageu]["time"] = time
	messageus[messageu]["date"] = date

	data["users"] = user
	data1["message"] = messageus

	with open("info.json", "w", encoding='utf8') as EditInfoJsonData:
		json.dump(data, EditInfoJsonData, indent=3, ensure_ascii=False)
	EditInfoJsonData.close()

	with open("message.json", "w", encoding='utf8') as EditMessageJsonData:
		json.dump(data1, EditMessageJsonData, indent=3, ensure_ascii=False)
	EditMessageJsonData.close()


def markup_inline():

	markup = InlineKeyboardMarkup()
	markup.width = 2
	markup.add(
		InlineKeyboardButton("button name", callback_data="prv"),
		InlineKeyboardButton("button name", callback_data="abt")
	)

	markup.add(
		InlineKeyboardButton("button name", callback_data="upd")
	)

	return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

	if call.data == "prv":
		bot.send_message(call.message.chat.id, text_messages["prv"])

	if call.data == "abt":
		photo = open('#src your photo', 'rb')
		bot.send_photo(call.message.chat.id, photo, caption=text_messages["about"])

	if call.data == "upd":
		bot.send_message(call.message.chat.id, text_messages["upd"])


# بداية تشغيل البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):

	firstname = message.from_user.first_name

	bot.reply_to(message, text_messages["get started"].format(firstname=firstname), parse_mode="Markdown", reply_markup=markup_inline())


# عند الدخول للمجموعة
@bot.my_chat_member_handler()
def hello_in_group(message: types.ChatMemberUpdated):
	update = message.new_chat_member
	if update.status == "member":
		bot.send_message(message.chat.id, text_messages["leavegroup"])
		bot.leave_chat(message.chat.id)


# الرد على الرسالة
@bot.message_handler(func=lambda message: True)
def echo_all(message):

	saveInfo(message=message)

	try:

		user_input = message.text

		message_input = []

		message_input.append({"role": "user", "content": user_input})

		completion = openai.ChatCompletion.create(

			model="gpt-3.5-turbo-0301",
			messages=message_input

		)

		reply_content = completion.choices[0].message.content

		bot.reply_to(message, reply_content)

	except:

		bot.reply_to(message, text_messages["no bot"])


def main():
	bot.infinity_polling(allowed_updates=util.update_types)


if __name__ == '__main__':
	main()
