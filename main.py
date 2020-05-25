# -*- coding: utf-8 -*-
import telebot
import config
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from telebot import types
from TexSoup import TexSoup
from database import engine, Task, Exam, meta, Answers
from sqlalchemy.orm import mapper, sessionmaker

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


@bot.callback_query_handler(func=lambda call: str(call.data).isdigit())
def answer_parser(answer):
    bot.send_message(answer.message.chat.id, answer.data)
    tmp_res[answer.from_user.username][user_question_num[answer.from_user.username]] = answer.data
    print(answer)
    bot.answer_callback_query(answer.id)
    sol_ex4(answer)



@bot.callback_query_handler(func=lambda call: call.data == 'p' or call.data == 's')
def user_parser(message):
    if True:
        if message.data == 'p':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Текущие тесты")
            item2 = types.KeyboardButton("Создать тест")
            item3 = types.KeyboardButton("Выгрузить результаты")

            markup.add(item1, item2)
            markup.add(item3)

            bot.send_message(message.message.chat.id, "Выберите необходимое действие", reply_markup=markup)
            bot.answer_callback_query(message.id)
        elif message.data == 's':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мои тесты")
            item2 = types.KeyboardButton("Решить тест")

            markup.add(item1, item2)

            bot.send_message(message.message.chat.id, "Выберите необходимое действие", reply_markup=markup)
            bot.answer_callback_query(message.id)
        else:
            bot.send_message(message.message.chat.id, "Попробуйте еще раз")


@bot.message_handler(func=lambda message: flag_file, content_types=['text'])
def save_ex(mes):
    global flag_file
    if mes.text == "Сохранить экзамен":
        flag_file = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Текущие тесты")
        item2 = types.KeyboardButton("Создать тест")
        item3 = types.KeyboardButton("Выгрузить результаты")

        markup.add(item1, item2)
        markup.add(item3)
        bot.send_message(mes.chat.id, "Экзамен успешно сохранен", reply_markup=markup)
    elif mes.text == "Изменить экзамен":
        Session = sessionmaker(bind=engine)
        Session = Session()
        last_exam = Session.query(Exam).filter_by(author=mes.from_user.username).all()[-1]
        Session.query(Task).filter_by(exam_id=last_exam.exam_id).delete(synchronize_session=False)
        Session.query(Exam).filter_by(exam_id=last_exam.exam_id).delete(synchronize_session=False)
        Session.commit()
        bot.send_message(mes.chat.id, "Заново загрузите все файлы")

        # здесь я пропишу удаление последнего экзамена созданного юзером
        # В идеале конечно чтобы он мог один или несколько файлов удалять


@bot.message_handler(content_types=['text'])
def callback_inline(call):
    try:
        Session = sessionmaker(bind=engine)
        Session = Session()
        if call.chat.type == 'private':
            if call.text == "Мои тесты":
                bot.send_message(call.chat.id, 'Здесь пройденные тесты студента')
            elif call.text == "Решить тест":
                id_ex = bot.send_message(call.chat.id, 'Введите идентификатор экзамена')
                bot.register_next_step_handler(id_ex, sol_ex1)
            elif call.text == 'Текущие тесты':
                exams = Session.query(Exam).filter_by(author=call.from_user.username).all()
                if len(exams) == 0:
                    bot.send_message(call.chat.id, 'У вас нет созданных тестов')
                else:
                    var = ''
                    for ex in exams:
                        var += ex.exam_id + '\n'
                    id_ex = bot.send_message(call.chat.id, 'Введите имя теста\n\nВозможные варианты:\n' + var)
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


usertmp = dict()

def create_exam(id_exam):
    exam = Exam(id_exam)
    exam.task_num = 0
    markup = types.ForceReply(selective=False)
    password = bot.send_message(id_exam.chat.id, 'Придумайте пароль для экзамена', reply_markup=markup)
    usertmp[id_exam.chat.id] = exam
    bot.register_next_step_handler(password, create_ex_2)

#flag_file = dict()

def create_ex_2(password):
    print("SP", password.text)
    exam = usertmp[password.chat.id]
    usertmp[password.chat.id] = None
    exam.password = password.text
    Session = sessionmaker(bind=engine)
    Session = Session()

    Session.add(exam)
    Session.commit()
    print(password.text)

    global flag_file
    flag_file = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сохранить экзамен")
    item2 = types.KeyboardButton("Изменить экзамен")
    markup.add(item1, item2)
    bot.send_message(password.chat.id, 'Загрузите пожалуйста необходимое число вопросов в latex формате', reply_markup=markup)
    #bot.register_next_step_handler(resp, )



@bot.message_handler(func=lambda message: flag_file, content_types=['document'])
def create_task(file):
    if file.document:
        Session = sessionmaker(bind=engine)
        Session = Session()
        raw = file.document.file_id
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(raw+".tex", 'wb') as new_file:
            new_file.write(downloaded_file)
        last_exam = Session.query(Exam).filter_by(author=file.from_user.username).all()[-1]
        last_exam.tasks_num += 1
        task = Task(TexSoup(open(raw+".tex").read()), last_exam.exam_id)
        bot.send_message(file.chat.id, task.question)
        #exam.task_list.append(task)
        #print(exam.task_list)


        Session.add(task)
        Session.commit()



def show_exams(id_ex):
    Session = sessionmaker(bind=engine)
    Session = Session()
    try:
        exam = Session.query(Exam).filter_by(author=id_ex.from_user.username, exam_id=id_ex.text).all()[0]
        out = 'Название экзамена - ' + str(exam.exam_id)
        out += '\nПароль экзамена - ' + exam.password
        out += '\nВсего заданий - ' + str(exam.tasks_num)
        out += '\nВсего прошло тест - ' + str(exam.number_of_res)
        out += '\n\nДля более подробных результатов нажмите выгрузить результаты'
        bot.send_message(id_ex.chat.id, out)
    except:
        bot.send_message(id_ex.chat.id, "Нет такого экзамена")





def sol_ex1(id_ex):
    Session = sessionmaker(bind=engine)
    Session = Session()
    try:
        print(id_ex.text)
        _ = Session.query(Exam).filter_by(exam_id=id_ex.text).all()[0]
        password = bot.send_message(id_ex.chat.id, "Введите пароль от экзамена")
        usertmp[id_ex.chat.id] = id_ex.text
        bot.register_next_step_handler(password, sol_ex2)
    except:
        bot.send_message(id_ex.chat.id, "Нет такого экзамена")


def sol_ex2(password):
    Session = sessionmaker(bind=engine)
    Session = Session()
    ex = Session.query(Exam).filter_by(exam_id=usertmp[password.chat.id]).all()[0]
    if ex.password != password.text: # или уже решал экзамен, или уже закрыт экзамен
        bot.send_message(password.chat.id, "Пароль не верный")
    else:
        check = bot.send_message(password.chat.id, "На экзамен дается одна попытка\nКак только будете готовы, напишите \"+\"")
        bot.register_next_step_handler(check, sol_ex3)


tmp_task_lst = dict()
user_question_num = dict()
tmp_res = dict()


def sol_ex3(check):
    if check.text != '+':
        bot.send_message(check.chat.id, "Выберите дальнейшее действие")
    else:
        Session = sessionmaker(bind=engine)
        Session = Session()
        ex = Session.query(Exam).filter_by(exam_id=usertmp[check.chat.id]).all()[0]
        tasks = list(Session.query(Task).filter_by(exam_id=usertmp[check.chat.id]).all())
        tmp_task_lst[check.from_user.username] = tasks
        user_question_num[check.from_user.username] = 0
        try:
            task = tasks[0]
            markup = types.InlineKeyboardMarkup(row_width=2)
            item_list = list(map(str, task.answerlist.split('\item')))[1:]
            for choos in range(len(item_list)):
                item = types.InlineKeyboardButton(item_list[choos][:-2], callback_data=str(choos))
                markup.add(item)
            ans = bot.send_message(check.chat.id, task.question, reply_markup=markup)
            tmp_res[check.from_user.username] = dict()
            print("sdgerhdf")
            #bot.register_next_step_handler(ans, sol_ex4)
        except:
            bot.send_message(check.chat.id, "Вопросов нет")



def sol_ex4(ans):
    print(ans)
    try:
        print("fdkjgh")
        print(tmp_res)
        user_question_num[ans.from_user.username] += 1
        task = tmp_task_lst[ans.from_user.username][user_question_num[ans.from_user.username]]
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_list = list(map(str, task.answerlist.split('\item')))[1:]
        for choos in range(len(item_list)):
            item = types.InlineKeyboardButton(item_list[choos][:-2], callback_data=str(choos))
            markup.add(item)
        ans = bot.send_message(ans.message.chat.id, task.question, reply_markup=markup)
    except:
        bot.send_message(ans.message.chat.id, "Экзамен закончен")
        sol_ex5(ans)


def sol_ex5(ans):
    Session = sessionmaker(bind=engine)
    Session = Session()

    for i in range(user_question_num[ans.from_user.username]):
        answer = tmp_res[ans.from_user.username][i]
        username = ans.from_user.username
        exam_id = tmp_task_lst[ans.from_user.username][i].exam_id
        correct_answer = tmp_task_lst[ans.from_user.username][i].exsolution.find('1')
        print(correct_answer)
        tmp_ans = Answers(exam_id, username, answer, correct_answer)
        Session.add(tmp_ans)

    Session.commit()




# RUN

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)