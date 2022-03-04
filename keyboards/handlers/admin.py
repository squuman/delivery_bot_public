from elements.messages import *
import aiogram.types as types
import resources
from resources import *


async def show_list_users(callback_query: types.CallbackQuery):
    users_list = user_handler.get_users_list()
    for user in users_list:
        await callback_query.message.reply(f"{user[2]}", reply=False)


async def add_user(callback_query: types.CallbackQuery):
    create_password = password_handler.create_password()
    await callback_query.message.reply(MessagesElements.NEW_PASSWORD_WAS_CREATED, reply=False)
    await callback_query.message.reply(create_password, reply=False)


async def delete_user(callback_query: types.CallbackQuery):
    await resources.BotStates.DELETE_USER.set()
    await callback_query.message.reply(MessagesElements.CHOOSE_USER, reply=False,
                                       reply_markup=admin_keyboards.delete_user_keyboard())


async def add_admin(callback_query: types.CallbackQuery):
    await resources.BotStates.ADD_ADMIN.set()
    await callback_query.message.reply(MessagesElements.CHOOSE_USER, reply=False,
                                       reply_markup=admin_keyboards.add_admin_keyboard())


async def delete_admin(callback_query: types.CallbackQuery):
    await resources.BotStates.DELETE_ADMIN.set()
    await callback_query.message.reply(MessagesElements.CHOOSE_USER, reply=False,
                                       reply_markup=admin_keyboards.delete_admin_keyboard())


async def show_list_admins(callback_query: types.CallbackQuery):
    admins_list = user_handler.get_admin_list()
    for admin in admins_list:
        await callback_query.message.reply(f"{admin[2]}", reply=False)
    await callback_query.message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                                       reply_markup=admin_keyboards.admin_keyboard())


async def back(callback_query: types.CallbackQuery):
    await callback_query.message.reply(MessagesElements.YOU_RETURN_TO_PROCESS_STATE, reply=False)
    await resources.BotStates.SEND_ORDER_DATA.set()


async def back_to_admin(callback_query: types.CallbackQuery):
    await callback_query.message.reply(MessagesElements.ADMIN, reply=False)
    await resources.BotStates.ADMIN.set()


async def delete_user_handler(callback_query: types.CallbackQuery, callback_data: dict):
    user_id = callback_data['user_id']
    if user_handler.update_user(user_id, {'is_delete': 1}) is True:
        await callback_query.message.reply(MessagesElements.DELETE_USER_SUCCESS)
        await resources.BotStates.ADMIN.set()
        await callback_query.message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                                           reply_markup=admin_keyboards.admin_keyboard())
    else:
        await callback_query.message.reply(MessagesElements.DELETE_USER_FAIL)


async def add_admin_handler(callback_query: types.CallbackQuery, callback_data: dict):
    user_id = callback_data['user_id']
    check_is_admin = admin_handler.check_is_admin(user_id)
    if check_is_admin is True:
        await callback_query.message.reply(MessagesElements.USER_ALREADY_IS_ADMIN)
    else:
        if user_handler.update_user(user_id, {'is_admin': 1}) is True:
            await callback_query.message.reply(MessagesElements.ADD_ADMIN_SUCCESS)
            await callback_query.message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                                               reply_markup=admin_keyboards.admin_keyboard())
            await resources.BotStates.ADMIN.set()
        else:
            await callback_query.message.reply(MessagesElements.ADD_ADMIN_FAIL)


async def delete_admin_handler(callback_query: types.CallbackQuery, callback_data: dict):
    user_id = callback_data['user_id']
    if user_handler.update_user(user_id, {'is_admin': 0}) is True:
        await callback_query.message.reply(MessagesElements.DELETE_ADMIN_SUCCESS)
        await callback_query.message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                                           reply_markup=admin_keyboards.admin_keyboard())
        await resources.BotStates.ADMIN.set()
    else:
        await callback_query.message.reply(MessagesElements.DELETE_ADMIN_FAIL)


async def back_to_admin(callback_query: types.CallbackQuery):
    await callback_query.message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                                       reply_markup=admin_keyboards.admin_keyboard())
    await resources.BotStates.ADMIN.set()
