from mailing import mailing
import requests
import tokens
import json
import api
import db
import functions
import crypto
import files
import db
import mailing
connect = db.connect()
#def course_messages(connect, course):

result = mailing.mailing(connect, token_hash, course, user_ids)
print(new_messages)

"""token_hash = "bmX6PNUNl6tdOhDRNPZ4NzFOGP19VAg19CODmauHdOE1Iw==*tITKwcgio74uYSgY2AhKOA==*wPngqZ63oZtIWkmSNrjpQQ==*tC5O3In7Po63CXQ5Jl+PZQ=="

message = 'Проверка связи!' # {'message': 'Привет!', 'attachment': []}
attachment = 'photo-98390003_457239180'
user_ids = [493087766]
timestamp = 1619982853

utc = str(datetime.fromtimestamp(1629999953))
msg = {'message': message, 'attachment': [attachment]}
data_object = {'message': msg, 'user_ids': user_ids, 'run_at': utc}
data = json.dumps(data_object)
headers = {'content-type': 'application/json'}
token = tokens.token_decode(token_hash)
url = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=' + token
answer = requests.post(url, data=data, headers=headers)
answer = mailing(connect, token_hash, "mm", user_ids)
print(answer)"""

"""token = "bdacb71ec6df8a7c7a05316e2b7ceda206dc436bf21b53b919bdf8257d0d9a2e842142cc71281e6a082dc"
token_hash = crypto.get_encode(token, "14870")


group_token_path = files.config("settings.conf", "group_token")
passwd = files.config("settings.conf", "token_pass")
token_array = files.read_to_list(group_token_path)
token_hash = token_array[0]
token = crypto.get_decode(token_hash, passwd)
response = api.report("message", 493087766, token)
print(response)"""