from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import resources
from elements.messages import *
import handlers.users as user_handler
import handlers.admin as admin_handler


def admin_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_ADD_USER, callback_data='add_user'))
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_DELETE_USER, callback_data='delete_user'))
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_USERS_LIST, callback_data='users_list'))
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_ADD_ADMIN, callback_data='add_admin'))
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_DELETE_ADMIN, callback_data='delete_admin'))
    keyboard.add(InlineKeyboardButton(MessagesElements.ADMIN_ADMINS_LIST, callback_data='admins_list'))
    keyboard.add(InlineKeyboardButton(MessagesElements.BACK_TO_ADMIN, callback_data='back'))

    return keyboard


def delete_user_keyboard():
    users_list = user_handler.get_users_list()
    keyboard = InlineKeyboardMarkup()
    for user in users_list:
        keyboard.add(
            InlineKeyboardButton(user[2],
                                 callback_data=resources.admin_panel_aim_user.new(user[1], 'delete_user_by_id')))
    keyboard.add(
        InlineKeyboardButton('Назад',
                             callback_data=resources.admin_panel_aim_user.new(user_id=0, action='back_to_admin')))

    return keyboard


def add_admin_keyboard():
    users_list = user_handler.get_users_list()
    keyboard = InlineKeyboardMarkup()

    for user in users_list:
        if user[5] == 0:
            keyboard.add(
                InlineKeyboardButton(f'{user[2]}',
                                     callback_data=resources.admin_panel_aim_user.new(user_id=user[1],
                                                                                      action='add_admin')))
    keyboard.add(
        InlineKeyboardButton('Назад',
                             callback_data=resources.admin_panel_aim_user.new(user_id=0, action='back_to_admin')))

    return keyboard


def delete_admin_keyboard():
    admins_list = admin_handler.get_admin_list()
    keyboard = InlineKeyboardMarkup()

    for admin in admins_list:
        print(admin)
        keyboard.add(InlineKeyboardButton(f'{admin[2]}',
                                          callback_data=resources.admin_panel_aim_user.new(admin[1], 'delete_admin')))
    keyboard.add(
        InlineKeyboardButton('Назад',
                             callback_data=resources.admin_panel_aim_user.new(user_id=0, action='back_to_admin')))

    return keyboard
