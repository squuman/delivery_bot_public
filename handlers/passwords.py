import random
import string

import mysql.connector
from config import *

connection = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database

)
cursor = connection.cursor()
table = 'passwords'


def check_password(password):
    print(get_password(password))
    if get_password(password):
        if get_password(password)[0][2] == 0:
            return True
        else:
            return False
    else:
        return False


def create_password():
    try:
        new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        cursor.execute(f"insert into passwords(value, is_use) values('{new_password}', 0)")
        connection.commit()

        return new_password
    except Exception as e:
        print(f'error {e}')


def get_password(password):
    try:
        cursor.execute(f"select * from {table} where value like '{password}' and is_use not like 1")
        return cursor.fetchall()
    except Exception as e:
        return [f'error {e}']


def update_password(password, is_use_value):
    try:
        cursor.execute(f"update {table} set is_use = {is_use_value} where value like '{password}'")
        connection.commit()
    except Exception as e:
        print([f'error {e}'])
