import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    #sti = open('./sticker.webp', 'rb')
    #bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.InlineKeyboardMarkup(row_width=2)
    teacher = types.InlineKeyboardButton("Преподаватель", callback_data='p')
    student = types.InlineKeyboardButton("Студент", callback_data='s')
    markup.add(teacher, student)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>!\nБот созданный для проверки домашних заданий".format(message.from_user, bot.get_me()),
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
                bot.send_message(call.chat.id, 'Здесь тесты созданные преподавателем')
            elif call.text == 'Создать тест':
                bot.send_message(call.chat.id, 'Здесь интерфейс для создания теста')
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

# RUN

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)