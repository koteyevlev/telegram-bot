import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}


class User:
    def __init__(self, surname, name, group=1):
        self.surname = surname
        self.name = name
        # group == 1 -- teacher
        self.group = group


@bot.message_handler(commands=['start'])
def welcome(message):
    #sti = open('./sticker.webp', 'rb')
    #bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    teacher = types.KeyboardButton("Преподаватель")
    student = types.KeyboardButton("Студент")
    markup.add(teacher, student)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>!\nБот созданный для проверки домашних заданий".format(message.from_user,bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def user_parser(message):
    if message.chat.type == 'private':
        if message.text == 'Преподаватель':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Мои тесты", callback_data='test_teach')
            item2 = types.InlineKeyboardButton("Создать тест", callback_data='create_test')
            item3 = types.InlineKeyboardButton("Выгрузить результаты", callback_data='results')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, "*Интерфейс для преподователя*", reply_markup=markup)
        elif message.text == 'Студент':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Мои тесты", callback_data='test_data')
            item2 = types.InlineKeyboardButton("Решить тест", callback_data='new_test')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "*Интерфейс для студента*", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Попробуйте еще раз")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'test_data':
                bot.send_message(call.message.chat.id, 'Здесь пройденные тесты студента')
            elif call.data == 'new_test':
                bot.send_message(call.message.chat.id, 'Здесь интерфейс для прохождения теста по id')
            elif call.data == 'test_teach':
                bot.send_message(call.message.chat.id, 'Здесь тесты созданные преподавателем')
            elif call.data == 'create_test':
                bot.send_message(call.message.chat.id, 'Здесь интерфейс для создания теста')
            elif call.data == 'results':
                bot.send_message(call.message.chat.id, 'Текущие результаты тестов')

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

# RUN

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)