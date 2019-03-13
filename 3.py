import telebot
import re


bot = telebot.TeleBot("706111907:AAHePLL-ZLh0FB26b2lzxGM5I3Q3vk2FTMQ")

#Обработчик команды '/help'
@bot.message_handler(commands=['help'])
def handle_help(message):
	help_message = """Привет!\nЯ - Бот Вагоновожатый и призван помочь тебе собирать инфу по обрывам в вагонах.\n
	Пользоваться мною просто - пиши мне сообщения формата:\n 01234 о111 д2-2 ф3,3,3 т\n
	И все будет круто!\n Пожалуйста, старайся не ошибаться, так как на данном этапе у меня нет возможности редактирования. 
	Тем более не стоит спамить. И никогда, НИКОГДА бл не шли мне смайлики!\n
	Чтобы получить файл с собранными данными - пришли мне команду /file\n"""
	bot.send_message(message.from_user.id, help_message)


# Обработчик команды '/start'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    pass
	
#Обработчик команды '/file'. По запросу предоставляет файл с собранными данными.
@bot.message_handler(commands=['file'])
def give_the_file(message):
	f1 = open('text.doc', 'r')
	bot.send_document(message.from_user.id, f1)
	f1.close()
	
#Обработчик сообщений. Принимает, преобразовывает и сохраняет в файл данные.
@bot.message_handler(content_types=["text"])
def handle_text(message):
	f = open('text.doc', 'a')
	new_text = re.sub(r'о', 'Окна: ', message.text.lower())
	new_text = re.sub(r'т', 'Торец, ', new_text)
	new_text = re.sub(r'ф', 'Форточки: ', new_text)
	new_text = re.sub(r'д', 'Двери: ', new_text)
	f.write('Вагон ' + new_text + '\n')
	f.close()
	
	
bot.polling(none_stop=True, interval=0)

