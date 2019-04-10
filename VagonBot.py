import telebot
import re
import schedule


bot = telebot.TeleBot('622604901:AAGY1a7fczTzmD-ugGsIdMPhtQp1MR6nqgg')


f2 = open('workfile.doc', 'a')
f2.write('             Отчет по обрывам в вагонах             \n')
f2.close()

@bot.message_handler(commands=['start'])
def handle_start(message):
	def gimme():
		f1 = open('workfile.doc', 'r')
		bot.send_document('360941887', f1)
		bot.send_document('776757284', f1)
		f1.close()
	schedule.every().day.at("09:10").do(gimme)
	while 1:
		schedule.run_pending()

#Обработчик команды '/help'  и '/start'
@bot.message_handler(commands=['help'])
def handle_help(message):
	help_message = """Привет!\nЯ - Бот Вагоновожатый и призван помочь тебе собирать инфу по обрывам в вагонах.\n
	Пользоваться мною просто - пиши мне сообщения формата:\n к/с/з 01234 о1,1,1 д2,2 ф3,3,3 т\n
	, где к/с/з - линии СБЛ/ОТЛ/СПЛ соответственно. И все будет круто!\n Пожалуйста, старайся не ошибаться, так как на данном этапе у меня нет возможности редактирования. 
	Тем более не стоит спамить. И никогда, НИКОГДА бл не шли мне смайлики!\n
	Чтобы получить файл с собранными данными - пришли мне команду /file\n"""
	bot.send_message(message.from_user.id, help_message)

	

@bot.message_handler(commands=['id'])
def give_id(message):
	bot.send_message(message.from_user.id, message.from_user.id)

	
#Обработчик команды '/file'. По запросу предоставляет файл с собранными данными.
@bot.message_handler(commands=['file'])
def give_the_file(message):
	f1 = open('workfile.doc', 'r')
	bot.send_document(message.from_user.id, f1)
	f1.close()


#Обработчик сообщений. Принимает, преобразовывает и сохраняет в файл данные.
@bot.message_handler(content_types=["text"])
def handle_text(message):
	f = open('workfile.doc', 'a')
	new_text = re.sub(r'с', 'OTL: №', message.text.lower())
	new_text = re.sub(r'к', 'SBL: №', new_text)
	new_text = re.sub(r'з', 'SPL: №', new_text)
	new_text = re.sub(r'о', 'Окна: ', new_text)
	new_text = re.sub(r'т', 'Торец, ', new_text)
	new_text = re.sub(r'ф', 'Форточки: ', new_text)
	new_text = re.sub(r'д', 'Двери: ', new_text)
	f.write(new_text + '\n')
	f.close()


	
bot.polling(none_stop=True, interval=0)
