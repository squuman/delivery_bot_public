import time
import urllib.request
import retailcrm
from aiogram import types

import bot
import keyboards.order_keyboards
import resources
import config
from elements.messages import MessagesElements
from elements.statuses import Statuses

client = retailcrm.v5(config.retail_url, config.retail_key)


async def get_order_to_delivery(callback_query: types.CallbackQuery):
    orders = resources.BotStates.CURRENT_ORDERS['orders']
    print(orders)
    for order in orders:
        order_edit = client.order_edit({
            'id': order['id'],
            'status': Statuses.SEND_TO_DELIVERY,
        }, 'id', order['site'])
        response = order_edit.get_response()
        if response['success'] is True:
            await resources.BotStates.BOT.edit_message_text(chat_id=callback_query.message.chat.id,
                                                            message_id=callback_query.message.message_id,
                                                            text=MessagesElements.ORDER_WAS_TURN_TO_DELIVERY(
                                                                order['number']))
        else:
            await resources.BotStates.BOT.edit_message_text(chat_id=callback_query.message.chat.id,
                                                            message_id=callback_query.message.message_id,
                                                            text=MessagesElements.ORDER_WASNT_TURN_TO_DELIVERY(
                                                                order['number']))

        time.sleep(2)

    resources.BotStates.CURRENT_ORDERS = {
        'branch': None,
        'orders': list()
    }
    await back(callback_query)


async def back(callback_query):
    await resources.BotStates.SEND_ORDER_DATA.set()
    await callback_query.message.reply(
        text=MessagesElements.GO_TO_JOB, reply=False)
    resources.BotStates.CURRENT_ORDERS = {
        'branch': None,
        'orders': list()
    }


async def back_to_menu(callback_query):
    await resources.BotStates.SEND_ORDER_DATA.set()
    await edit_message(chat_id=callback_query.message.chat.id,
                       message_id=callback_query.message.message_id,
                       text=MessagesElements.GO_TO_JOB)
    # await callback_query.message.reply(
    #     text=MessagesElements.GO_TO_JOB, reply=False)
    resources.BotStates.CURRENT_ORDERS = {
        'branch': None,
        'orders': list()
    }


"""
ЕСЛИ к оплате 0р. ТО …. пишем о том что оплата не требуется и предлагаем закрыть заказ
Заказу проставляется статус выполнен и в боте он закрывается.

ЕСЛИ к оплате больше 0р. ТО … пишем о том что требуется оплата в таком то размере и предлагаем выбрать способ оплаты (текущий сценарий ОК)
Если наличные, то предлагаем завершить заказ, проставляем статус выполнен, закрываем заказ.
Если по ссылке, то формируем ссылку, отправляем клиенту, ждем, пока оплатит. проставляем статус выполнен заказа, закрываем заказ.

ЕСЛИ к оплате больше 0р. И стоит галочка “Постоплата” ТО … (текущий сценарий ОК)
Переводим заказ в статус выполнено и закрываем заказ.
"""


async def pickup(callback_query: types.CallbackQuery):
    order = resources.BotStates.CURRENT_ORDERS['orders'][-1]
    paid_sum = order['totalSumm'] - order['prepaySum']
    if paid_sum == 0:
        await resources.BotStates.PROCESS_PREPAY_ORDER.set()
        resources.BotStates.MESSAGE = await resources.BotStates.BOT.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=MessagesElements.PAYMENT_NOT_NEED,
            reply_markup=keyboards.order_keyboards.finish_prepay_order())
    if paid_sum > 0 and order['customFields']['a01f39e3c6'] is False:
        await resources.BotStates.CHOOSE_PAYMENT_METHOD.set()
        resources.BotStates.MESSAGE = await resources.BotStates.BOT.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=MessagesElements.ORDER_PAYMENT_AMOUNT(paid_sum) + " " + MessagesElements.CHOOSE_PAYMENT_METHOD,
            reply_markup=keyboards.order_keyboards.choose_payment_method(),
            parse_mode='Markdown')
        # await callback_query.message.reply(MessagesElements.CHOOSE_PAYMENT_METHOD, reply=False,
        #                                    reply_markup=keyboards.order_keyboards.choose_payment_method())
    if paid_sum > 0 and order['customFields']['a01f39e3c6'] is True:
        await resources.BotStates.PROCESS_PREPAY_ORDER.set()
        resources.BotStates.MESSAGE = await resources.BotStates.BOT.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=MessagesElements.PAYMENT_NOT_NEED,
            reply_markup=keyboards.order_keyboards.finish_prepay_order())


async def close_order(callback_query: types.CallbackQuery):
    await finish_order(callback_query)


async def pay_cash_order(callback_query: types.CallbackQuery):
    await resources.BotStates.FINISH_ORDER.set()
    await resources.BotStates.BOT.edit_message_text(chat_id=callback_query.message.chat.id,
                                                    message_id=callback_query.message.message_id,
                                                    text=MessagesElements.CASH_PAYMENT_WAS_CHOOSED,
                                                    reply_markup=keyboards.order_keyboards.finish_order())


async def finish_order(callback_query: types.CallbackQuery, send_finish=True):
    order = resources.BotStates.CURRENT_ORDERS['orders'][-1]
    order = client.order(order['id'], 'id', order['site']).get_response()['order']
    payments = order['payments']
    payment_edit_res = True
    for id in payments:
        if payments[id]['type'] == 'cash' and payments[id]['status'] != 'paid':
            payment_edit = client.order_payment_edit({
                'status': 'paid',
                'amount': payments[id]['amount'],
                'id': id
            }, 'id', order['site'])

            if payment_edit.is_successful() is False:
                payment_edit_res = False
            else:
                time.sleep(15)

    order_edit = client.order_edit({
        'id': order['id'],
        'status': Statuses.COMPLETE
    }, 'id', order['site'])

    if send_finish is True:
        if order_edit.is_successful() is True and payment_edit_res is True:
            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                               MessagesElements.ORDER_WAS_FINISHED(order['id']))
        else:
            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                               MessagesElements.ORDER_WASNT_FINISHED(order['id']))
    await back(callback_query)


async def pay_link_order(callback_query: types.CallbackQuery):
    order = resources.BotStates.CURRENT_ORDERS['orders'][-1]
    skip_delete = False
    delete_payment = False

    for payment in order['payments']:
        if 'status' in order['payments'][payment]:
            if order['payments'][payment]['status'] == 'paid' or order['payments'][payment]['type'] == 'sber-shop-1' or \
                    order['payments'][payment]['type'] == 'sber-shop-2':
                skip_delete = True
                continue
            delete_payment = client.order_payment_delete(payment)

            if delete_payment.is_successful() is True:
                delete_payment = True
            else:
                delete_payment = False

    if order['site'] == 'laitcom-ru':
        payment_type = 'sber-shop-1'
    else:
        payment_type = 'sber-shop-2'

    create_payment = client.order_payment_create({
        'amount': order['totalSumm'] - order['prepaySum'],
        'type': payment_type,
        'order': {
            'id': order['id']
        }
    }, order['site'])

    if (delete_payment is True and create_payment.is_successful() is True) or (
            skip_delete is True and create_payment.is_successful() is True):
        await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                           MessagesElements.PAYMENT_WAS_CREATED)

        create_invoice = client.payment_create_invoice({
            'paymentId': create_payment.get_response()['id']
        })

        if create_invoice.is_successful() is True:
            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                               MessagesElements.PAYMENT_LINK_WAS_CREATED)

            edit_order = client.order_edit({
                'id': order['id'],
                'customFields': {
                    'payment_link': create_invoice.get_response()['result']['link'],
                    'telegram_chat_id': callback_query.message.chat.id
                }
            }, 'id', order['site'])

            if edit_order.is_successful():
                await resources.BotStates.WAIT_PAYMENT.set()
                resources.BotStates.MESSAGE = await resources.BotStates.BOT.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=MessagesElements.CASH_PAYMENT_WAS_CHOOSED,
                    reply_markup=keyboards.order_keyboards.finish_order())

                counter = 0
                paid = False

                while True:
                    try:
                        resources.BotStates.MESSAGE = await resources.BotStates.BOT.edit_message_text(
                            chat_id=callback_query.message.chat.id,
                            message_id=callback_query.message.message_id,
                            text=MessagesElements.PAYMENT_LINK_WAS_PASS_TO_ORDER + " " + MessagesElements.WAIT_PAYMENT,
                            reply_markup=keyboards.order_keyboards.return_to_cash())
                    except Exception as e:
                        print(e)
                    time.sleep(2)
                    counter += 1
                    order = client.order(order['id'], 'id', order['site']).get_response()['order']
                    print(order)
                    payments = order['payments']

                    for id in payments:
                        if str(id) == str(create_payment.get_response()['id']):
                            if 'status' in payments[id]:
                                if payments[id]['status'] == 'paid':
                                    paid = True

                    if resources.BotStates.RETURN_TO_CASH is True:
                        break

                    print(paid)

                    if paid is True:
                        time.sleep(15)
                        order_edit = client.order_edit({
                            'id': order['id'],
                            'status': Statuses.COMPLETE
                        }, 'id', order['site'])
                        if order_edit.is_successful() is True:
                            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                                               MessagesElements.ORDER_WAS_PAID_AND_FINISHED(order['id']))
                            await resources.BotStates.SEND_ORDER_DATA.set()
                        else:
                            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                                               MessagesElements.SOMETHING_WRONG)
                        await callback_query.message.reply(MessagesElements.GO_TO_JOB, reply=False)
                        break
            else:
                await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                                   MessagesElements.PAYMENT_LINK_WASNT_PASS_TO_ORDER)
                await back(callback_query)
        else:
            await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                               MessagesElements.PAYMENT_LINK_WASNT_CREATED)
            await back(callback_query)
    else:
        await edit_message(callback_query.message.chat.id, callback_query.message.message_id,
                           MessagesElements.PAYMENT_WASNT_CREATED)
        await back(callback_query)


async def set_paid_payment_in_order(order):
    payments = order['payments']
    for id in payments:
        payment_edit = client.order_payment_edit({
            'id': id,
            'status': Statuses.PAID
        }, 'id', order['site'])

        if payment_edit.is_successful() is False:
            return False
    return True


async def finish_prepay_order(callback_query: types.CallbackQuery):
    await finish_order(callback_query)


async def edit_message(chat_id, message_id, text):
    try:
        await resources.BotStates.BOT.edit_message_text(chat_id=chat_id,
                                                        message_id=message_id,
                                                        text=text)
        time.sleep(2)
    except Exception as e:
        print(e)


async def return_to_cash(callback_query: types.CallbackQuery):
    resources.BotStates.RETURN_TO_CASH = True
    order = resources.BotStates.CURRENT_ORDERS['orders'][-1]

    create_payment = client.order_payment_create({
        'order': {
            'id': order['id']
        },
        'amount': order['totalSumm'],
        'type': 'cash',
        'status': 'not-paid',
    }, order['site'])

    print(create_payment.get_response())

    if create_payment.is_successful() is True:
        await pay_cash_order(callback_query)
    else:
        await callback_query.message.reply(MessagesElements.SOMETHING_WRONG)
