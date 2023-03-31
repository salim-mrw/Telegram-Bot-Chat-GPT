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
	"get started": u"واو *{firstname}* 😍 حسنا 😊 انت الان متصل بChat GPT يمكنك البدء بالتحدث او الاطلاع على الاقسام التالية 😎🎉\n\n.",
	"about": u"هذا البوت من انتاج فريق NIT 🌍\n\nصنع سنة 2023 🌟\n\nبواسطة @salim_mrw 💙\n\nيقدم هذا البوت خدمات Chat GPT لتحسين تجربة المستخدمين داخل تيليكرام وهو احد تقنيات الذكاء الاصطناعي المشهورة حيث تستطيع من خلاله على سبيل المثال\n\n🔵 تنقيح النصوص\n\n🔵 المساعدة في برمجة المواقع والتطبيقات\n\n🔵 ضمان جودة البرمجيات\n\n🔵 كتابة كلمة سر صعبة الاختراق\n\n🔵 تحري السرقة الادبية\n\n🔵 المساعدة في الترويج على منصات التواصل الاجتماعي\n\n🔵 اجراء محاكاة للمقابلات الوظيفية\n\n🔵 المساعدة في كتابة رسائل البريد الالكتروني\n\n🔵 كتابة الخطابات التحفيزية\n\n🔵 كتابة القصص\n\n🔵 القيام بدور المستشار الوظيفي\n\n🔵 المساعدة في ادارة الشؤون المالية\n\n🔵 الحصول على النطق الصحيح لكلمات اللغة الانكليزية\n\n🔵 المساعدة في اختيار اسم للعلامة التجارية\n\n.",
	"leavegroup": u"سعيد لأضافتي هنا ☺\n\nلكن قد تتسبب التقنية التي لدي ببعض المشاكل داخل مجتمعكم 🥲\n\nحيث اني مبرمج على تنفيذ ما يطلب مني 😉\n\nارجو المعذرة انا مضطر للمغادرة انتظركم هنا 🙂\n\n@ChatGPT_Arab_bot 🎤\n\n.",
	"prv": u"نحن بصفتنا مساعد ذكي ، نحرص على حماية خصوصية مستخدمينا ونحرص على الحفاظ على سرية معلوماتهم الشخصية. لذلك ، نقدر ثقتك بنا ونحن نتعهد بحماية خصوصية معلوماتك الشخصية.\n\nيتم جمع المعلومات التي تحتفظ بها أداة المساعد الذكي عبر بوت Chat GPT والتي هي ضرورية لتحسين الخدمة وتجربة المستخدم. تتضمن هذه المعلومات التي يتم جمعها الاسم واسم المستخدم والمعرف واخر ظهور وغير ذلك الكثير. كل هذه المعلومات تستخدم فقط لأغراض إحصائية داخلية ولن يتم مشاركتها مع أي طرف ثالث.\n\nنحن نستخدم تقنيات الأمان المناسبة والمتعارف عليها صناعيًا لحماية المعلومات الشخصية المخزنة والتي يتم جمعها من خلال بوت Chat GPT. نتخذ جميع التدابير المتوفرة لحماية هذه المعلومات من الوصول غير المصرح به\n\nنحن نحتفظ بالحق في تغيير سياسة الخصوصية هذه في أي وقت ودون إشعار مسبق. سيتم تحديث هذه الرسالة بمجرد حدوث أي تغييرات، وعلاوة على ذلك يتم نشر النسخة الحالية من هذه السياسة على القسم الخاص بالتحديثات. من المستحسن عليك التحقق من هذا القسم بشكل دوري للاطلاع على أحدث سياسة خصوصية لبوت Chat GPT.\n\nإذا كان لديك أي أسئلة أو استفسارات حول سياسة الخصوصية لبوت Chat GPT ، فيرجى الاتصال بنا عبر البريد الإلكتروني. نحن نتطلع إلى الاستماع منك وتقديم المساعدة في أي وقت.\n\nالبريد الالكتروني\n\nchatgpt.telebot@gmail.com\n\n.",
	"upd": u"سيتم اضافة موديل GPT 4 قريبا جدا 😍",
	"no bot": u"البوت تحت الصيانة ولا يوجد استجابة من Chat GPT حاليا شكرا لتفهمكم 💙\n\n."
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
		InlineKeyboardButton("سياسة الخصوصية 😉", callback_data="prv"),
		InlineKeyboardButton("حول البوت 😎", callback_data="abt")
	)

	markup.add(
		InlineKeyboardButton("اخر التحديثات 🥰", callback_data="upd")
	)

	return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

	if call.data == "prv":
		bot.send_message(call.message.chat.id, text_messages["prv"])

	if call.data == "abt":
		photo = open('img/1.png', 'rb')
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
