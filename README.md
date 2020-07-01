# Телеграм бот для организации контрольных работ 

Бота зовут hse_checkbot :blush:. С его помощью можно создавать и решать контрольные работы. Все созданные экзамены и результаты решений бот записывает в базу данных.

## Содержание репозитория. 
В репозитории хранится основной код для работы с ботом:
1. Код для запуска телеграм бота.
2. Код для установки базы данных.
3. Примеры вопросов для контрольных работ.

## Инструкция для установки бота.
Для установки бота на локальную машину нужно:
1. Клонировать репозиторий на копмьютер.
    * Можно клонировать репозиторий через кнопку ***clone or download*** на главной страницы репозитория.
    * Можно клонировать репозиторий через консоль, с помощью команды `git clone https://github.com/koteyevlev/telegram-bot `.
После этого в домашней папке появится папка репозитория.
2. Далее нужно установить все необходимые библиотеки. 
`pip install -r requirements.txt`
3. Далее нужно запустить main.py. 

## Инструкция для создания базы данных. 
1. На первом шаге нужно установить MySQL. Файл для установки можно скачать на официальном сайте https://dev.mysql.com/downloads/mysql/. 
 Можно установить MySQL через консоль. Напрример, для Linux нужно использовать команду `sudo apt-get install mysql-server`.
2. На этапе установки нужно создать пользователя для базы данных. Если устанавливать базу данных через веб-сайт, то во всплывающем окне нужно будет придумать логин и пароль для пользователя. 
3. Далее нужно создать нужную базу данных `create database telegram_bot`.
4. Далее в database.py в элемент db_string нужно передавать логин, пароль от пользователя и название базы данных (по дефолту пользователь и пароль root). 
5. Нужно запустить database.py. 

! Стоит запускать файлы без VPN. 


Более подробную инструкцию по установке бота на компьютер можно посмотреть по ссылке: https://www.youtube.com/watch?v=XuPCQq5rEk4
Также доступны видео для установки бота на удаленный сервер https://www.youtube.com/watch?v=Xx89CV7jl8w и демострация работы бота https://www.youtube.com/watch?v=uczqc6-Bzq8 
