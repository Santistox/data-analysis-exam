# -*- coding: utf-8 -*-

import re
import telebot
import config
import dbworker
import random
import string
from time import gmtime, strftime, sleep

bot = telebot.TeleBot(config.token)

# function generate user code
def gen_code(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

# function log user messages to log files and admin chat
def log(time, message):
	log_print(time, message.from_user.username, message.chat.id, message.text)
	bot.send_message(509291958, '@{} send(id{}):\n\'{}\''.format(message.from_user.username, message.chat.id, message.text))

# function print log to file
def log_print(time, user, user_id, command):
	log_file = open('message_log.txt', 'a')
	log_file.write('{}:@{}({}) \"{}\"\n'.format(time, user, user_id, command))
	log_file.close()

''' 

	Bot commands

'''
# function handles /start command
@bot.message_handler(commands=["start"])
def cmd_start(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Welcome to AnalisBot, {}'.format(message.from_user.first_name))
	bot.send_message(message.chat.id, 'Отправь свой ключ и я тебе помогу решить экзамен!\n\nНужна помощь?\nНажми сюда: /help\n\nНет ключа?\nНажми сюда: /buykey')
	bot.send_message(509291958, 'added new user, @{}\nchatid: {}'.format(message.from_user.username, message.chat.id))
	bot.send_message(568371117, 'added new user, @{}\nchatid: {}'.format(message.from_user.username, message.chat.id))
	dbworker.set_state(message.chat.id, config.States.S_KEY.value)

# function handles /reset command
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, "Что ж, начнём по-новой. Отправь ключ?")
	dbworker.set_state(message.chat.id, config.States.S_KEY.value)

# function handles /codegen command
@bot.message_handler(commands=['codegen'])
def code_generation(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	if message.chat.id == 568371117 or message.chat.id == 509291958:
		code = gen_code(8)
		dbworker.set_key(code, 1)
		if dbworker.get_key_info(code) == '1':
			bot.send_message(message.chat.id, 'Code generated successful\n')
			bot.send_message(message.chat.id, code)
		else:
			bot.send_message(message.chat.id, 'Oh shit, something going wrong, report was sent\n')
			return
	else:
		bot.send_message(message.chat.id, 'Атата‼️\n\nТолько для админов!\n')
		return

# function handles /help command
@bot.message_handler(commands=['help'])
def help_message(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	help_output = 'Этот бот самый лучший и быстрый способ сдать экзамен по АНАЛизу Данных!\n\n'
	help_output += 'Купи ключ за 100₽, отправь его мне, скинь свои задания и ты получишь готовый файл с ответами и подробным решением!\n\n'
	help_output += 'Как только я пойму что ключ активный, я тебе задам пару вопросов и ты получишь свое решение!\n\n'
	help_output += 'Группа поддержки и там где купить ключ https://vk.com/public196319329\n\n'
	help_output += 'Удачи на экзамене!'
	bot.send_message(message.chat.id, help_output)

# function handles /buykey command
@bot.message_handler(commands=['buykey'])
def help_message(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	help_output = 'Этот бот самый лучший и быстрый способ сдать экзамен по АНАЛизу Данных!\n\n'
	help_output += 'Что бы использовать бота, купи ключ, он стоит 100₽ и покупается в группе, а потом приходи ко мне за инструкциями\n\n'
	help_output += 'Как только я пойму что ключ активный, я тебе задам пару вопросов и ты получишь свое решение!\n\n'
	help_output += 'Группа поддержки и там где купить ключ https://vk.com/public196319329'
	bot.send_message(message.chat.id, help_output)

# function handles /status command
@bot.message_handler(commands=['status'])
def status_message(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	status_output = 'STATUS:\n🟢Online\n'
	status_output += 'Server datatime: '
	status_output += strftime("%Y-%m-%d %H:%M:%S", gmtime())
	status_output += '\nActive tasks: preformance ({}%)✅'.format(random.randint(1, 100))
	status_output += '\nYour chatId: '
	status_output += str(message.chat.id)
	status_output += '\nBot version: v1.0.0 Build 1906.47812'
	status_output += '\nBot by member of TBHTA - Telegram Bots High Tech Alliance'
	bot.send_message(message.chat.id, status_output)

# function handles /fix command
@bot.message_handler(commands=['fix'])
def fix_message(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)


# take key from user
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_KEY.value)
def get_key_from_user(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Пытаюсь распознать твой ключ...');
	print(dbworker.get_key_info(message.text))
	if int(dbworker.get_key_info(message.text)) > 0:
		dbworker.use_key(message.text)
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALxY17ml19ost0i90xYz_w9yP_vDDV7AAJCAANQV40QVWWRW7A7JYEaBA')
		bot.send_message(message.chat.id, 'Твой ключ настоящий!!!\n\nИ у тебе еще {} попыток!!!'.format(dbworker.get_key_info(message.text)))
		bot.send_message(message.chat.id, 'Теперь слушай сюда!\nЧтобы все было гладко выполняй все строго по интсрукции!!')
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALxZV7mnE5tOPjvLOtWe2lzKPzQ7jW1AAJdAAMK_MIFZjRMJxxv1nIaBA')
		bot.send_message(message.chat.id, '**Первая часть**')
		# ask dataset from task1
		bot.send_message(message.chat.id, 'Возьми данные как показано на картинке и отправь сюда')
		bot.send_photo(message.chat.id, open('./service_images/task1.png', 'rb'))
		dbworker.set_state(message.chat.id, config.States.S_TASK1_DATASET.value)
	else:
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALxYV7ml1q5EiXyy-mHZcASeJ9PibpEAAJIAANQV40Qv8jEnTZjskMaBA')
		bot.send_message(message.chat.id, 'Мне жаль, но я не знаю такого ключа(((\n\nНо ты можешь купить ключ,он стоит всего 100₽!!!\n\nЧтобы это сделать, тыкни /buykey')

''' 

	TASKS PART

'''

# task1 variant
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK1_DATASET.value)
def task1_1(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Какой из этих 3х вопросов у тебя?')
	bot.send_photo(message.chat.id, open('./service_images/task1_1_1.png', 'rb'))
	bot.send_photo(message.chat.id, open('./service_images/task1_1_2.png', 'rb'))
	bot.send_photo(message.chat.id, open('./service_images/task1_1_3.png', 'rb'))
	bot.send_message(message.chat.id, 'Отправь 1, 2 или 3')
	dbworker.set_state(message.chat.id, config.States.S_TASK1_Q3.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK1_Q3.value)
def task1_2(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	print(message.text)
	if int(message.text) < 1 or int(message.text) > 3:
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\n\nОтправь 1, 2 или 3")
		return
	else:
		if int(message.text) == 1:
			bot.send_message(message.chat.id, 'Чему равен квантиль в 19 задании?\n\nЧилсо вида 0.85')
			bot.send_photo(message.chat.id, open('./service_images/task1_2.png', 'rb'))
			dbworker.set_state(message.chat.id, config.States.S_TASK1_KRVTL.value)
		else:
			bot.send_message(message.chat.id, '**Вторая часть**')
			bot.send_message(message.chat.id, 'Возьми данные как показано на картинке и отправь сюда')
			bot.send_photo(message.chat.id, open('./service_images/task2.png', 'rb'))
			dbworker.set_state(message.chat.id, config.States.S_TASK2_DATASET.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK1_KRVTL.value)
def task1_2(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	if re.match(r'^-?\d+(?:\.\d+)?$', message.text) is None:
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\n\nЧилсо вида 0.85")
		return
	else:
		bot.send_message(message.chat.id, '**Вторая часть**')
		bot.send_message(message.chat.id, 'Возьми данные как показано на картинке и отправь сюда')
		bot.send_photo(message.chat.id, open('./service_images/task2.png', 'rb'))
		dbworker.set_state(message.chat.id, config.States.S_TASK2_DATASET.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_DATASET.value)
def task2_1(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Какой из этих 2х вопросов у тебя?\n\nОтправь 1 или 2')
	bot.send_photo(message.chat.id, open('./service_images/task2_1_1.png', 'rb'))
	bot.send_photo(message.chat.id, open('./service_images/task2_1_2.png', 'rb'))
	dbworker.set_state(message.chat.id, config.States.S_TASK2_Q1.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_Q1.value)
def task2_2(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	if int(message.text) < 1 or int(message.text) > 2:
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\n\nОтправь 1 или 2")
		return
	else:
		bot.send_message(message.chat.id, 'Чему равна граница в 5 задании?\n\nЧилсо вида 0.9')
		bot.send_photo(message.chat.id, open('./service_images/task2_5_1.png', 'rb'))
		dbworker.set_state(message.chat.id, config.States.S_TASK2_BRDR.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_BRDR.value)
def task2_3(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	if re.match(r'^-?\d+(?:\.\d+)?$', message.text) is None:
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\n\nЧилсо вида 0.9")
		return
	else:
		bot.send_message(message.chat.id, 'Для какого ответа просят границу в 5 задании?')
		bot.send_photo(message.chat.id, open('./service_images/task2_5_2.png', 'rb'))
		bot.send_message(message.chat.id, 'Введи ТОЧНО также как в задании!')
		dbworker.set_state(message.chat.id, config.States.S_TASK2_BRDR_WD.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_BRDR_WD.value)
def task2_4(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Для какого ответа просят границу в 4 задании?')
	bot.send_photo(message.chat.id, open('./service_images/task2_4.png', 'rb'))
	bot.send_message(message.chat.id, 'Введи ТОЧНО также как в зажании!')
	dbworker.set_state(message.chat.id, config.States.S_TASK2_WD.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_WD.value)
def task2_5(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Чему равен уровнь значимости?\n\nЧилсо вида 0.01')
	bot.send_photo(message.chat.id, open('./service_images/task2_6.png', 'rb'))
	dbworker.set_state(message.chat.id, config.States.S_TASK2_LVL.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK2_LVL.value)
def task2_6(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	if re.match(r'^-?\d+(?:\.\d+)?$', message.text) is None:
		bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!\n\nЧилсо вида 0.01")
		return
	else:
		bot.send_message(message.chat.id, '**Третья часть**')
		bot.send_message(message.chat.id, 'Возьми данные как показано на картинке и отправь сюда')
		bot.send_photo(message.chat.id, open('./service_images/task3.png', 'rb'))
		dbworker.set_state(message.chat.id, config.States.S_TASK3_DATASET.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TASK3_DATASET.value)
def task3_3(message):
	log(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message)
	bot.send_message(message.chat.id, 'Ты красавчик!\n\nОсталось только правильно перенести ответы!')
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALxZ17mnv8T8gJ53bX6EZ4v9Mo5oXOgAALNGwAClju6F_j9cZ8iZQaKGgQ')
	bot.send_message(message.chat.id, 'Собираю файл\n\nПримерно 10 секунд\n\nПошу терпения!')
	sleep(10)
	bot.send_document(message.chat.id, open('./works/test.xlsx', 'rb'))
	dbworker.set_state(message.chat.id, config.States.S_KEY.value)



bot.polling()
