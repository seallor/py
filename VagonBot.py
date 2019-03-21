import telebot
import re
import schedule


bot = telebot.TeleBot('622604901:AAGY1a7fczTzmD-ugGsIdMPhtQp1MR6nqgg')


f2 = open('workfile.doc', 'a')
f2.write('----\n')
f2.close()


#Обработчик команды '/help'  и '/start'
@bot.message_handler(commands=['help', 'start'])
def handle_help(message):
	help_message = """Привет!\nЯ - Бот Вагоновожатый и призван помочь тебе собирать инфу по обрывам в вагонах.\n
	Пользоваться мною просто - пиши мне сообщения формата:\n л/б/п 01234 о111 д2-2 ф3,3,3 т\n
	, где л/б/п - линии ОТЛ/СБЛ/СПЛ соответственно. И все будет круто!\n Пожалуйста, старайся не ошибаться, так как на данном этапе у меня нет возможности редактирования. 
	Тем более не стоит спамить. И никогда, НИКОГДА бл не шли мне смайлики!\n
	Чтобы получить файл с собранными данными - пришли мне команду /file\n"""
	bot.send_message(message.from_user.id, help_message)


#Обработчик команды '/restart'.
@bot.message_handler(commands=['restart'])
def handle_restart(message):
	f1 = open('workfile.doc', 'r')
	bot.send_document(message.from_user.id, f1)
	f1.close()
	f1 = open('workfile.doc', 'w')
	f1.write('-------------------------Отчёт по обрывам в вагонах----------------------------'+ '\n')
	f1.close()


#Обработчик команды '/gimme_file'.
@bot.message_handler(commands=['gimme_file'])
def file_by_time(message):
	def gimme():
		f1 = open('workfile.doc', 'r')
		bot.send_document(message.from_user.id, f1)
		f1.close()
		
	schedule.every().day.at("18:30").do(gimme)
	
	while 1:
		schedule.run_pending()
	

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
	new_text = re.sub(r'л', 'OTL: №', message.text.lower())
	new_text = re.sub(r'б', 'SBL: №', new_text)
	new_text = re.sub(r'п', 'SPL: №', new_text)
	new_text = re.sub(r'о', 'Окна: ', new_text)
	new_text = re.sub(r'т', 'Торец, ', new_text)
	new_text = re.sub(r'ф', 'Форточки: ', new_text)
	new_text = re.sub(r'д', 'Двери: ', new_text)
	f.write(new_text + '\n')
	f.close()


bot.polling(none_stop=True, interval=0)
