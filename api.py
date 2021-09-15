import requests
import files

# Получение статуса рассылки
def status(token):
    url = "https://broadcast.vkforms.ru/api/v2/broadcast?token=" + token
    code = {}
    data = dict(code=code, access_token=token)
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    answer = resp.json()
    return answer


# Получение списка пользователей:
def users(token, list):
    sting = "https://broadcast.vkforms.ru/api/v2/list/" + str(list) + "?format=json&token=" + token
    response = requests.get(sting)
    return response


# Получение данных пользователей:
def userdata(token, user_ids):
    uid_string = []
    for uid in user_ids:
        uid_string.append(uid)
    uid_str = ','.join(map(str, uid_string))
    fields = 'last_seen,sex,bdate,city,country,contacts,site,status,has_photo,photo_200'
    version = '5.130'
    response = requests.get('https://api.vk.com/method/users.get',
                            params={'access_token': token,
                                    'user_ids': uid_str,
                                    'fields': fields,
                                    'v': version
                                    }
                            )
    return response.json()


# Отправка сообщений администратору
def report(message, user_id, token):
    version = '5.126'
    response = requests.get('https://api.vk.com/method/messages.send',
                            params={'access_token': token,
                                    'message': message,
                                    'user_id': user_id,
                                    'v': version
                                    }
                            )
    return response.json()