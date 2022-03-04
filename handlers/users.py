import mysql.connector
from config import *

connection = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database

)
cursor = connection.cursor()

table = 'users'


def check_exists(id):
    if get_user(id):
        return True
    else:
        return False


def get_users_list():
    try:
        cursor.execute(f'select * from {table} where is_delete not like 1')
        return cursor.fetchall()
    except Exception as e:
        return [f'error {e}']


def get_admin_list():
    try:
        cursor.execute(f'select * from {table} where is_delete not like 1 and is_admin like 1')
        return cursor.fetchall()
    except Exception as e:
        return [f'error {e}']


def get_user(id):
    try:
        cursor.execute(f'select * from {table} where tel_id like {id} and is_delete not like 1')
        return cursor.fetchall()
    except Exception as e:
        return [f'error {e}']


def create_user(data):
    try:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`"
                            for x in data.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'"
                           for x in data.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)

        cursor.execute(sql)
        connection.commit()

        return True
    except Exception as e:
        print(e)
        return False


def update_user(id, data):
    try:
        columns = ', '.join(str(x).replace('/', '_') + " = " + f"{str(data[x])}"
                            for x in data.keys())
        sql = "update %s SET %s where tel_id like %s;" % (table, columns, id)

        cursor.execute(sql)
        connection.commit()

        return True
    except Exception as e:
        print(e)
        return False
