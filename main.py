import telebot
from google_drive_downloader import GoogleDriveDownloader as gdd
import config

from telebot import types
from TexSoup import TexSoup

bot = telebot.TeleBot(config.TOKEN)
flag_file = False

@bot.message_handler(commands=['start'])
def welcome(message):
    #sti = open('./sticker.webp', 'rb')
    #bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    teacher = types.InlineKeyboardButton("Преподаватель", callback_data='p')
    student = types.InlineKeyboardButton("Студент", callback_data='s')
    markup.add(teacher, student)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>!\nБот созданный для проверки домашних заданий".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'p' or call.data == 's')
def user_parser(message):
    if True:
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                              text="Выберите необходимое действие",
                              reply_markup=None)
        if message.data == 'p':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Текущие тесты")
            item2 = types.KeyboardButton("Создать тест")
            item3 = types.KeyboardButton("Выгрузить результаты")

            markup.add(item1, item2)
            markup.add(item3)

            bot.send_message(message.message.chat.id, "*Интерфейс для преподователя*", reply_markup=markup)
            bot.answer_callback_query(message.id)
        elif message.data == 's':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мои тесты")
            item2 = types.KeyboardButton("Решить тест")

            markup.add(item1, item2)

            bot.send_message(message.message.chat.id, "*Интерфейс для студента*", reply_markup=markup)
            bot.answer_callback_query(message.id)
        else:
            bot.send_message(message.message.chat.id, "Попробуйте еще раз")


@bot.message_handler(content_types=['text'])
def callback_inline(call):
    try:
        if call.chat.type == 'private':
            if call.text == "Мои тесты":
                bot.send_message(call.chat.id, 'Здесь пройденные тесты студента')
            elif call.text == "Решить тест":
                bot.send_message(call.chat.id, 'Здесь интерфейс для прохождения теста по id')
            elif call.text == 'Текущие тесты':
                id_ex = bot.send_message(call.chat.id, 'Введите имя теста')
                bot.register_next_step_handler(id_ex, show_exams)
            elif call.text == 'Создать тест':
                id_exam = bot.send_message(call.chat.id, 'Пожалуйста придумайте уникальный идентификатор для экзамена')
                bot.register_next_step_handler(id_exam, create_exam)
            elif call.text == "Выгрузить результаты":
                bot.send_message(call.chat.id, 'Текущие результаты тестов')
            # remove inline buttons
            #if call.data == 'test_data' or call.data == 'new_test':
            #    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Студент",
            #                          reply_markup=None)
            #else:
            #    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Преподаватель",
            #                          reply_markup=None)

            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                          text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


class Task:
    def __init__(self, soup):
        self.question = soup.question
        self.answerlist = list(soup.question.answerlist.find_all('item'))
        self.solution = soup.solution
        self.exname = soup.exname
        self.extype = soup.extype
        self.exsolution = soup.exsolution
        self.exshuffle = soup.exshuffle


class Exam:
    def __init__(self, data):
        self.author = data.from_user.username
        self.id_exam = data.text
        self.participants = None
        self.task_list = []

exam = None

def create_exam(id_exam):
    global exam
    print(id_exam)
    exam = Exam(id_exam)
    participants = bot.send_message(id_exam.chat.id, 'Перечислите ники в телеграмме у участников')
    exam.participants = list(participants.text.split(','))
    bot.register_next_step_handler(id_exam, create_ex_2)


def create_ex_2(id_exam):
    global flag_file
    resp = bot.send_message(id_exam.chat.id, 'Загрузите пожалуйста необходимое число вопросов в latex формате')
    flag_file = True
    bot.register_next_step_handler(resp, is_continue)


def is_continue(resp):
    #global exam
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Сохранить экзамен", callback_data="save")
    item2 = types.InlineKeyboardButton("Изменить экзамен", callback_data="change")
    markup.add(item1, item2)
    bot.send_message(resp.chat.id,
                     "Хотите ли вы сохранить экзамен или что-то изменить? Если хотите еще загрузить файл, просто продолжайте загружать",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: flag_file, content_types=['document'])
def create_task(file):
    #global exam
    if file and file.document:
        raw = file.document.file_id
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(raw+".tex", 'wb') as new_file:
            new_file.write(downloaded_file)
        task = Task(TexSoup(open(raw+".tex").read()))
        #markup = types.InlineKeyboardMarkup(row_width=3)
        #for i in range(len(task.answerlist)):
        #    item = types.InlineKeyboardButton(str(task.answerlist[i])[6:], callback_data=str(i))
        #    markup.add(item)
        #bot.send_message(file.chat.id, task.question, reply_markup=markup)
        exam.task_list.append(task)
        print(exam.task_list)

def show_exams(id_ex):
    out = []
    print(exam.task_list)
    for i in exam.task_list:
        out.append(i.question)
    print(*out)
    bot.send_message(id_ex.chat.id, len(out))

# RUN

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)