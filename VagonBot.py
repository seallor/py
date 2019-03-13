import telebot
import re


bot = telebot.TeleBot("")


#Обработчик команды '/help'  и '/start'
@bot.message_handler(commands=['help', 'start'])
def handle_help(message):
	help_message = """Привет!\nЯ - Бот Вагоновожатый и призван помочь тебе собирать инфу по обрывам в вагонах.\n
	Сначала выбери линию командой /sbl /spl или /otl.\n
	Дальше пользоваться мною просто - пиши мне сообщения формата:\n 01234 о111 д2-2 ф3,3,3 т\n
	И все будет круто!\n Пожалуйста, старайся не ошибаться, так как на данном этапе у меня нет возможности редактирования. 
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


#Обработчик команды СБЛ
@bot.message_handler(commands=['sbl'])
def sbl_line(message):
	f = open('workfile.doc', 'a')
	f.write('-------------------------------------СБЛ---------------------------------------' + '\n')
	f.close()


#Обработчик команды ОТЛ
@bot.message_handler(commands=['otl'])
def otl_line(message):
	f = open('workfile.doc', 'a')
	f.write('-------------------------------------ОТЛ---------------------------------------' + '\n')
	f.close()


#Обработчик команды СПЛ
@bot.message_handler(commands=['spl'])
def spl_line(message):
	f = open('workfile.doc', 'a')
	f.write('-------------------------------------СПЛ---------------------------------------' + '\n')
	f.close()
	


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
	new_text = re.sub(r'о', 'Окна: ', message.text.lower())
	new_text = re.sub(r'т', 'Торец, ', new_text)
	new_text = re.sub(r'ф', 'Форточки: ', new_text)
	new_text = re.sub(r'д', 'Двери: ', new_text)
	f.write('Вагон ' + new_text + '\n')
	f.close()


bot.polling(none_stop=True, interval=0)

