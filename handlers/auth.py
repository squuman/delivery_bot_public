from resources import *


def check_auth(id):
    print(user_handler.get_user(id))
    if user_handler.get_user(id)[0][4] == 0:
        return False
    else:
        return True


def login(user_id, password):
    check_password = password_handler.check_password(password)

    if check_password is True:
        user_handler.update_user(user_id, {'is_auth': 1})
        password_handler.update_password(password, 1)
        return True
    else:
        return False


def logout(user_id):
    logout = user_handler.update_user(user_id, {'is_auth': 0})
    if logout is True:
        return True
    else:
        return False
