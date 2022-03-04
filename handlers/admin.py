from resources import *
from config import *

connection = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database

)
cursor = connection.cursor()

table = 'users'


def check_is_admin(user_id):
    if user_handler.check_exists(user_id):
        if user_handler.get_user(user_id)[0][6] == 0:
            return False
        else:
            return True
    else:
        return False


def get_admin_list():
    try:
        cursor.execute(f'select * from {table} where is_delete not like 1 and is_admin like 1')
        return cursor.fetchall()
    except Exception as e:
        return [f'error {e}']
