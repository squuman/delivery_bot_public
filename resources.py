import logging
import asyncio
import mysql.connector
from aiogram.utils.callback_data import CallbackData

import handlers.users as user_handler
import handlers.passwords as password_handler
import handlers.auth as auth_handler
import handlers.photo as photo_handler
import handlers.order as order_handler
import handlers.scanner as scanner_handler
import handlers.admin as admin_handler
import keyboards.admin_keyboards as admin_keyboards
import keyboards.order_keyboards as order_keyboards
import keyboards.handlers.admin as admin_keyboard_handler
import keyboards.handlers.order as order_keyboard_handler
from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import bot, dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Dispatcher
from config import *
from elements.messages import *

bot = bot.Bot(dev_token)
dp = dispatcher.Dispatcher(bot, storage=MemoryStorage())
connection = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database

)
cursor = connection.cursor()

admin_panel_aim_user = CallbackData('data', 'user_id', 'action')


class BotStates(StatesGroup):
    MESSAGE = None
    BOT = None

    START = State()
    AUTH = State()
    ADMIN = State()
    DELETE_USER = State()
    ADD_ADMIN = State()
    DELETE_ADMIN = State()

    CHOOSE_ACTION = State()

    SEND_ORDER_DATA = State()

    IN_PROCESS = State()

    GET_TO_DELIVERY = State()

    PICKUP = State()
    PICKUP_ORDER_PAID = State()
    CHOOSE_PAYMENT_METHOD = State()
    FINISH_ORDER = State()
    WAIT_PAYMENT = State()
    PROCESS_PREPAY_ORDER = State()

    DELIVERY = State()

    RETURN_TO_CASH = None

    CURRENT_ORDERS = {
        'branch': None,
        'orders': list()
    }
