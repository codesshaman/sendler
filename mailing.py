from datetime import datetime
from random import randint
import requests
import tokens
import json
import db

# Функция мгновенной отправки сообщения
def mailing_now(token_hash, user_ids, message):
    msg = {'message': message}
    data_object = {'message': msg, 'user_ids': user_ids, 'run_now': 1}
    data = json.dumps(data_object)
    headers = {'content-type': 'application/json'}
    token = tokens.token_decode(token_hash)
    url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
    answer = requests.post(url, data=data, headers=headers)
    return answer


# Функция мгновенной отправки сообщения с прикрепом
def mailing_now_att(token_hash, user_ids, message, attachment):
    msg = {'message': message, 'attachment': [attachment]}
    data_object = {'message': msg, 'user_ids': user_ids, 'run_now': 1}
    data = json.dumps(data_object)
    headers = {'content-type': 'application/json'}
    token = tokens.token_decode(token_hash)
    url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
    answer = requests.post(url, data=data, headers=headers)
    return answer


# Функция отложенной отправки сообщения
def mailing_timing(token_hash, user_ids, message, time):
    utc = str(datetime.fromtimestamp(time))
    msg = {'message': message}
    data_object = {'message': msg, 'user_ids': user_ids, 'run_at': utc}
    data = json.dumps(data_object)
    headers = {'content-type': 'application/json'}
    token = tokens.token_decode(token_hash)
    url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
    answer = requests.post(url, data=data, headers=headers)
    return answer


# Функция отложенной отправки сообщения с прикрепом
def mailing_timing_att(token_hash, user_ids, message, attachment, time):
    utc = str(datetime.fromtimestamp(time))
    msg = {'message': message, 'attachment': [attachment]}
    data_object = {'message': msg, 'user_ids': user_ids, 'run_at': utc}
    data = json.dumps(data_object)
    headers = {'content-type': 'application/json'}
    token = tokens.token_decode(token_hash)
    url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
    answer = requests.post(url, data=data, headers=headers)
    return answer


# Отбор сообщений курса
def course_messages(connect, course):
    course_array = db.find(connect, "db_name", "courses", "_id", "mm")
    messages_ids = course_array["messages"]
    new_messages = []
    for msg_id in messages_ids:
        message_object = db.find(connect, "db_name", "messages", "_id", msg_id)
        message_array = message_object["message"]
        separator = message_object["separator"]
        message = separator.join(message_array)
        attachment = message_object["attachments"]
        msg_obj = [[message], attachment]
        new_messages.append(msg_obj)
    return new_messages


# Создание рассылки
def mailing(connect, token_hash, course, user_ids):
    messages = course_messages(connect, course)
    twelve = 43200
    counter = 0
    time = round(datetime.now().timestamp())
    for message in messages:
        time += twelve
        random = randint(0, 14400)
        send_time = time + random
        utc = str(datetime.fromtimestamp(send_time))
        msg = {'message': message[0], 'attachment': [message[1]]}
        data_object = {'message': msg, 'user_ids': user_ids, 'run_at': utc}
        data = json.dumps(data_object)
        headers = {'content-type': 'application/json'}
        token = tokens.token_decode(token_hash)
        url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
        answer = requests.post(url, data=data, headers=headers)
        print(answer)
        time += twelve
        counter += 1
    print("Запланировано " + str(counter) + " сообщений.")