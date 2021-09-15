import random
import files
import crypto


def tokens_settings():
    tokens_list = []
    password = files.config('settings.conf', 'token_pass')
    token_list = files.read_to_list("tokensfile.txt")
    for token in token_list:
        tkn = crypto.get_decode(token, password)
        tokens_list.append(tkn)
    return tokens_list


def token(list, prew):
    length = len(list) - 1
    index = random.randint(0, length)
    counter = True
    while counter:
        if index == prew:
            counter = True
            index = random.randint(0, length)
        else:
            counter = False
    return index


def expenditure(list):
    exp = []
    for i in list:
        exp.append(0)
    return exp


def token_decode(token_hash):
    password = files.config('settings.conf', 'token_pass')
    result = crypto.get_decode(token_hash, password)
    return result