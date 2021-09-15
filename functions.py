import db


# Функция формирования данных пользователя для сохранения
def user_save(user, course):
    set = {}
    set['_id'] = user["id"]
    set['name'] = user['first_name']
    set['last_name'] = user['last_name']
    set['sex'] = user['sex']
    if 'bdate' in user:
        set['bdate'] = user['bdate']
    if 'city' in user:
        set['city'] = user['city']['id']
    if 'city' in user:
        set['city_name'] = user['city']['title']
    if 'country' in user:
        set['country'] = user['country']['id']
    if 'country' in user:
        set['country_name'] = user['country']['title']
    if 'status' in user:
        if len(user['status']) > 0:
            set['status'] = user['status'].replace("'", '"').replace('\n', ' ')
    if 'contacts' in user:
        set['contacts'] = user['contacts']
    if 'site' in user:
        if len(user['site']) > 0:
            set['site'] = user['site']
    if 'mobile_phone' in user:
        if len(user['mobile_phone']) > 0:
            set['mobile_phone'] = user['mobile_phone']
    if 'home_phone' in user:
        if len(user['home_phone']) > 0:
            set['home_phone'] = user['home_phone']
    if 'last_seen' in user:
        set['last_seen'] = user['last_seen']['time']
        if 'platform' in user['last_seen']:
            set['platform'] = user['last_seen']['platform']
    set['courses'] = [course]
    set['courses_counter'] = 1
    return set


# Функция добавления курса в список курсов пользователя
def user_append(connect, user_id, course):
    userdata = db.find(connect, "db_name", "subscribers", "_id", user_id)
    counter = userdata["courses_counter"]
    counter += 1
    db.push(connect, "db_name", "subscribers", "_id", user_id, "courses", course)
    db.update(connect, "db_name", "subscribers", "_id", user_id, "courses_counter", counter)


# Функция удаления курса из списка курсов пользователя
def user_remove(connect, user_id, course):
    userdata = db.find(connect, "db_name", "subscribers", "_id", user_id)
    courses_counter = userdata["courses_counter"]
    counter = courses_counter - 1
    db.pull(connect, "db_name", "subscribers", "_id", user_id, "courses", course)
    db.update(connect, "db_name", "subscribers", "_id", user_id, "courses_counter", counter)


# Функция добавления новых пользователей в список курса
def course_add(connect, user_id, course):
    data = db.find(connect, "db_name", "courses", "_id", course)
    counter = data["counter"]
    counter += 1
    db.push(connect, "db_name", "courses", "_id", course, "users", user_id)
    db.update(connect, "db_name", "courses", "_id", course, "counter", counter)


# Функция удаления отписавшихся из списка курса
def course_rem(connect, user_id, course):
    data = db.find(connect, "db_name", "courses", "_id", course)
    counter = data["counter"]
    counter -= 1
    db.pull(connect, "db_name", "courses", "_id", course, "users", user_id)
    db.update(connect, "db_name", "courses", "_id", course, "counter", counter)


# Функция поиска курса
def course_find(connect, course_name):
    return db.check(connect, "db_name", "courses", "_id", course_name)


# Функция поиска пользователя
def user_find(connect, user_id):
    return db.check(connect, "db_name", "subscribers", "_id", user_id)


# Получение пользователей курса
def course_users(connect, name):
    return db.find(connect, "db_name", "courses", '_id', name)