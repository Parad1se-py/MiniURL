from utility.database import *

def check_login_info(username:str, password:str):
    docs = get_all_docs()

    for i in docs:
        if i['_id'] == username:
            if i['password'] == password:
                return True
            else:
                return [False, "Wrong password or username provided"]
    return [False, "Wrong password or username provided"]