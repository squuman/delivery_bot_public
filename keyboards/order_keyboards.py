from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from elements.messages import *


def for_shipment():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.GET_ORDER_TO_DELIVERY, callback_data='get_to_delivery_menu_get')).add(
        InlineKeyboardButton(
            MessagesElements.TO_START, callback_data='back_to_menu'))


def for_pickup():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.CHECK_PAYMENT, callback_data='pickup_get')).add(InlineKeyboardButton(
        MessagesElements.TO_START, callback_data='pickup_back'))


def close_order():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.CLOSE_ORDER, callback_data='close_order'))


def choose_payment_method():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.CASH, callback_data='payment_type_cash')).add(
        InlineKeyboardButton(MessagesElements.LINK, callback_data='payment_type_link')).add(
        InlineKeyboardButton(MessagesElements.TO_START, callback_data='back_to_menu'))


def finish_order():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.FINISH_ORDER, callback_data='finish_order')).add(
        InlineKeyboardButton(MessagesElements.TO_START, callback_data='back_to_menu'))


def finish_prepay_order():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.FINISH_ORDER, callback_data='finish_prepay_order')).add(
        InlineKeyboardButton(MessagesElements.TO_START, callback_data='back_to_menu'))


def return_to_cash():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(MessagesElements.RETURN_TO_CASH, callback_data='return_to_cash'))