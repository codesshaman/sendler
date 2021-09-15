#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db
import api
import json
import files
import crypto
import tokens
import mailing
import functions

# Соединяюсь с базой
connect = db.connect()

# Обрабатываю список токенов
tokens_list = tokens.tokens_settings()
preview = 0
exp = tokens.expenditure(tokens_list)
print(exp)

# Получаю токен сообщества
group_token_path = files.config("settings.conf", "group_token")
passwd = files.config("settings.conf", "token_pass")
token_array = files.read_to_list(group_token_path)
token_hash = token_array[0]
community_token = crypto.get_decode(token_hash, passwd)

# Получаю список курсов
check = db.data(connect, "db_name", "courses", "_id", "list")
array = check[0]["list"]
courses_list = []

# Выбираю из списка курсов уже запущенные
for course in array:
    check = functions.course_find(connect, course)
    if check > 0:
        courses_list.append(course)

# Запускаю цикл
for course in courses_list:
    result = db.find(connect, "db_name", "courses", "_id", course)  # Запрашиваю все данные курса
    number = result["list"]  # Получаю номер рассылки
    id_list = result["users"]  # Получаю список id подписчиков
    id_length = len(id_list)  # Получаю число подписчиков
    token_hash = result["token"]  # Получаю хэш токена
    token = tokens.token_decode(token_hash)  # Декодирую хэш токена
    answer = api.users(token, number)  # Получаю текущих подписчиков
    if answer.status_code == 200:  # Если запрос прошёл успешно,
        content = answer.content  # Получаю содержимое запроса
        string = content.decode('utf-8')  # Перевожу из байтов в строку
        json_list = json.loads(string)  # Перевожу в формат json
        today = json_list["response"]  # Произвожу парсинг json
        unsubscribers = []  # Формирую список отписок
        subscribers = []  # Формирую список подписок


        """Этап 1. Удаление отписавшихся"""
        # Проверяю отписавшихся
        if len(id_list) > 0:  # Если есть id подписчиков,
            for user in id_list:  # Проверяю каждый из id
                if user not in today:  # И если он отсутствует
                    unsubscribers.append(user)  # Добавляем в список отписок
                    # Удаляем id пользователя из списка участников курса
                    functions.course_rem(connect, user, course)
                    # Удаляем id курса из данных пользователя
                    functions.user_remove(connect, user, course)

        if len(unsubscribers) > 0:
            print("Отписалось " + str(len(unsubscribers)) + " пользователей из курса " + course)
            message = "За сегодня " + str(len(unsubscribers)) + " отписавшихся от курса " + course + \
                      + ": " + str(subscribers)
            request = api.report(message, "493087766", community_token)
            print(request)
        """Этап 2. Добавление подписавшихся"""
        # Проверяю новых подписчиков
        if len(today) > 0:  # Если есть новые подписчики
            for user in today:  # Перебираем их в цикле
                if user not in id_list:  # Если подписчика нет в рассылке
                    subscribers.append(user)  # Добавляем в список новых подписок
                    functions.course_add(connect, user, course)

        # Если есть незанесённые в базу подписчики
        if len(subscribers) > 0:
            # Получаю рандомный токен
            token_index = tokens.token(tokens_list, preview)
            token = tokens_list[int(token_index)]
            preview = token_index
            exp[token_index] += 1
            # Получаю данные подписчиков
            answer = api.userdata(token, subscribers)
            response = answer["response"]
            for user in response:
                userdata = functions.user_save(user, course)
                check = functions.user_find(connect, userdata['_id'])
                if check == 0:
                    db.insert(connect, "db_name", "subscribers", userdata)
                if check == 1:
                    functions.user_append(connect, userdata['_id'], course)
            # Формирую тело рассылки
            mailing.mailing(connect, token_hash, course, subscribers)
            print("Добавлено " + str(len(subscribers)) + " подписчиков курса " + course)
            # Отправляю отчёт
            message = "За сегодня " + str(len(subscribers)) + " новых подписчиков курса " + course + ": " + str(subscribers)
            request = api.report(message, "493087766", community_token)
            print(request)
    # Если запрос не прошёл:
    else:
        print("Что-то не так с запросом")