import elements.statuses as statuses
import elements.delivery_types as delivery
from aiogram import types
from resources import *

logger = logging.getLogger(__name__)


# Начало цикла работы
# - Проверяется наличие юзера в бд.
# -- Если есть, то проверка его авторизации в боте
# --- Если авторизован, то дается допуск к интерфейсу работы
# --- Если нет, то запрашивается пароль
# -- Если нет пользователя в бд, то создается новый и переход к авторизации
async def start(message: types.Message):
    if user_handler.check_exists(message.from_user.id):
        if auth_handler.check_auth(message.from_user.id):
            await BotStates.SEND_ORDER_DATA.set()
            await message.reply(MessagesElements.GO_TO_JOB, reply=False)
        else:
            await BotStates.AUTH.set()
            await message.reply(MessagesElements.AUTH, reply=False)
    else:
        create_user = user_handler.create_user({
            'tel_id': message.from_user.id,
            'name': message.from_user.full_name,
            'username': message.from_user.username,
            'is_auth': 0,
            'is_admin': 0,
            'is_delete': 0,
        })
        if create_user is False:
            await message.reply(MessagesElements.CREATE_USER_FAIL, reply=False)
        else:
            await BotStates.AUTH.set()
            await message.reply(MessagesElements.AUTH, reply=False)


# Авторизация пользователя
#  - Проверка авторизации пользователя
#  -- Если пол. авторизирован, то приступает к работе
#  -- Иначе бот заправшивает пароль
async def send_auth_password(message: types.Message):
    auth_result = auth_handler.login(message.from_user.id, message.text)
    if auth_result is True:
        await message.reply(MessagesElements.AUTH_SUCCESS, reply=False)
        await BotStates.SEND_ORDER_DATA.set()
    else:
        await message.reply(MessagesElements.AUTH_FAIL, reply=False)


# Выход пользователя из бота
async def logout(message: types.Message):
    logout = auth_handler.logout(message.from_user.id)
    if logout is True:
        await message.reply(MessagesElements.LOGOUT_SUCCESS, reply=False)
    else:
        await message.reply(MessagesElements.LOGOUT_FAIL, reply=False)


# Вход в панель администратора. Могу войти лишь те, у кого есть доступ
async def admin(message: types.Message):
    if admin_handler.check_is_admin(message.from_user.id):
        await message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_ACCESS, reply=False,
                            reply_markup=admin_keyboards.admin_keyboard())
        await BotStates.ADMIN.set()
    else:
        await message.reply(MessagesElements.ADMIN_PANEL_PERMISSION_DENIED, reply=False)


# Прием данных о заказе: баркод или номер заказа.
# Вход в цикл обработки заказа
async def order_process(message):
    # register bot state
    BotStates.CURRENT_ORDERS['orders'] = list()
    BotStates.BOT = bot
    order_number = None
    # Распознаем данные заказа: его номер (равен id в срм). Такжэ очищаем от дублей, если такие есть.
    if 'text' in message:
        order_number = message.text.split(" ")
    elif 'photo' in message:
        photo_path = await photo_handler.save_photo(message['photo'][-1])
        scan_result = scanner_handler.read_barcode(photo_path)
        if scan_result is False:
            await message.reply(MessagesElements.ORDER_WASNT_SCAN, reply=False)
        else:
            order_number = str(scanner_handler.read_barcode(photo_path)[0]).replace("b'", '').replace('\'', '')
    else:
        await message.reply(MessagesElements.WRONG_DATA_TYPE)

    # Проверяем существование заказа (В случае неудачи выводим ошибку)
    # Записываем данные заказов в список состояния заказов.
    if order_number is not None:
        await BotStates.IN_PROCESS.set()
        # await message.reply(MessagesElements.START_ORDER_SEARCH, reply=False)
        for number in order_number:
            order = await order_handler.get_orders(number)
            if order:
                # await message.reply(MessagesElements.ORDER_WAS_FOUND(order_number), reply=False)
                BotStates.CURRENT_ORDERS['orders'].append(order.copy())
            else:
                await message.reply(MessagesElements.ORDER_WASNT_FOUND(number), reply=False)

        # Проверяем какому сценарию пренадлежит заказ
        if BotStates.CURRENT_ORDERS['orders']:
            orders = BotStates.CURRENT_ORDERS['orders']
            BotStates.CURRENT_ORDERS['orders'] = list()
            statuses_list = statuses.Statuses.get_statuses()
            for order in orders:
                if 'code' in order['delivery']:
                    if order['status'] == statuses.Statuses.FOR_SHIPMENT:
                        print('for shipment')
                        if order['delivery']['code'] != delivery.DeliveryTypes.SELF_DELIVERY:
                            BotStates.CURRENT_ORDERS['branch'] = 'for_shipment'
                            BotStates.CURRENT_ORDERS['orders'].append(order.copy())
                        else:
                            await message.reply(MessagesElements.DELIVERY_TYPE_CANT_BE_PICKUP, reply=False)
                    if order['status'] == statuses.Statuses.READY_TO_PICKUP:
                        print('pickup')
                        if order['delivery']['code'] == delivery.DeliveryTypes.SELF_DELIVERY:
                            BotStates.CURRENT_ORDERS['branch'] = 'pickup'
                            BotStates.CURRENT_ORDERS['orders'].append(order.copy())
                        else:
                            await BotStates.SEND_ORDER_DATA.set()
                            await message.reply(MessagesElements.DELIVERY_TYPE_MUST_BE_PICKUP, reply=False)
                            await message.reply(MessagesElements.GO_TO_JOB, reply=False)
                    if order['status'] == statuses.Statuses.SEND_TO_DELIVERY:
                        print('delivery')
                        BotStates.CURRENT_ORDERS['branch'] = 'delivery'
                        BotStates.CURRENT_ORDERS['orders'].append(order.copy())
                else:
                    return await message.reply(MessagesElements.DELIVERY_TYPE_NOT_CHOOSE, reply=False)

            print(BotStates.CURRENT_ORDERS['orders'])

            # В зависимости от сценария высылаем юзеру меню
            if BotStates.CURRENT_ORDERS['branch'] == 'for_shipment':
                await BotStates.GET_TO_DELIVERY.set()
                BotStates.MESSAGE = await message.reply(statuses_list['for-shipment']['name'],
                                                        reply_markup=order_keyboards.for_shipment(),
                                                        reply=False)

            if BotStates.CURRENT_ORDERS['branch'] == 'pickup' or BotStates.CURRENT_ORDERS['branch'] == 'delivery':
                if len(BotStates.CURRENT_ORDERS['orders']) > 1:
                    await BotStates.SEND_ORDER_DATA.set()
                    await message.reply(MessagesElements.I_CANT_PROCESS_FEW_ORDERS, reply=False)
                elif len(BotStates.CURRENT_ORDERS['orders']) == 1:
                    await BotStates.PICKUP.set()
                    status_message = None
                    if BotStates.CURRENT_ORDERS['branch'] == 'pickup':
                        status_message = statuses_list['fa86f52f50']['name']
                    else:
                        status_message = statuses_list['send-to-delivery']['name']
                    BotStates.MESSAGE = await message.reply(status_message,
                                                            reply_markup=order_keyboards.for_pickup(),
                                                            reply=False)
                elif len(BotStates.CURRENT_ORDERS['orders']) == 0:
                    await BotStates.SEND_ORDER_DATA.set()
                    await message.reply(MessagesElements.ZERO_ORDERS, reply=False)
        else:
            await message.reply(MessagesElements.NO_ONE_ORDER_HAD_BEEN_FIND, reply=False)
    else:
        await message.reply(MessagesElements.NO_ONE_ORDER_HAD_BEEN_SCAN, reply=False)
        await BotStates.SEND_ORDER_DATA.set()


# Регистрация обработчиков команд
def register_handlers(dp):
    # register commands handlers
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(send_auth_password, state=BotStates.AUTH)
    dp.register_message_handler(admin, commands='admin', state='*')
    dp.register_message_handler(order_process, content_types=['photo', 'text'], state=BotStates.SEND_ORDER_DATA)

    # register callback handlers
    dp.register_callback_query_handler(admin_keyboard_handler.show_list_users,
                                       lambda c: c.data and c.data.startswith('users_list'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.add_user,
                                       lambda c: c.data and c.data.startswith('add_user'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.delete_user,
                                       lambda c: c.data and c.data.startswith('delete_user'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.add_admin,
                                       lambda c: c.data and c.data.startswith('add_admin'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.delete_admin,
                                       lambda c: c.data and c.data.startswith('delete_admin'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.show_list_admins,
                                       lambda c: c.data and c.data.startswith('admins_list'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.back,
                                       lambda c: c.data and c.data.startswith('back'),
                                       state=BotStates.ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.back_to_admin,
                                       admin_panel_aim_user.filter(action='back_to_admin'),
                                       state=[BotStates.DELETE_USER, BotStates.DELETE_ADMIN, BotStates.ADD_ADMIN])

    # admin panel handlers
    dp.register_callback_query_handler(admin_keyboard_handler.delete_user_handler,
                                       admin_panel_aim_user.filter(action='delete_user_by_id'),
                                       state=BotStates.DELETE_USER)
    dp.register_callback_query_handler(admin_keyboard_handler.add_admin_handler,
                                       admin_panel_aim_user.filter(action='add_admin'),
                                       state=BotStates.ADD_ADMIN)
    dp.register_callback_query_handler(admin_keyboard_handler.delete_admin_handler,
                                       admin_panel_aim_user.filter(action='delete_admin'),
                                       state=BotStates.DELETE_ADMIN)

    # order for shipment handlers
    dp.register_callback_query_handler(order_keyboard_handler.get_order_to_delivery,
                                       lambda c: c.data and c.data.startswith('get_to_delivery_menu_get'),
                                       state=BotStates.GET_TO_DELIVERY)
    dp.register_callback_query_handler(order_keyboard_handler.back_to_menu,
                                       lambda c: c.data and c.data.startswith('back_to_menu'),
                                       state=BotStates.GET_TO_DELIVERY)

    # order for pickup handlers
    dp.register_callback_query_handler(order_keyboard_handler.pickup,
                                       lambda c: c.data and c.data.startswith('pickup_get'),
                                       state=BotStates.PICKUP)
    dp.register_callback_query_handler(order_keyboard_handler.back_to_menu,
                                       lambda c: c.data and c.data.startswith('pickup_back'),
                                       state=BotStates.PICKUP)
    dp.register_callback_query_handler(order_keyboard_handler.close_order,
                                       lambda c: c.data and c.data.startswith('close_order'),
                                       state=BotStates.PICKUP_ORDER_PAID)
    dp.register_callback_query_handler(order_keyboard_handler.pay_cash_order,
                                       lambda c: c.data and c.data.startswith('payment_type_cash'),
                                       state=BotStates.CHOOSE_PAYMENT_METHOD)
    dp.register_callback_query_handler(order_keyboard_handler.pay_link_order,
                                       lambda c: c.data and c.data.startswith('payment_type_link'),
                                       state=BotStates.CHOOSE_PAYMENT_METHOD)
    dp.register_callback_query_handler(order_keyboard_handler.back_to_menu,
                                       lambda c: c.data and c.data.startswith('back_to_menu'),
                                       state=BotStates.CHOOSE_PAYMENT_METHOD)
    dp.register_callback_query_handler(order_keyboard_handler.finish_order,
                                       lambda c: c.data and c.data.startswith('finish_order'),
                                       state=BotStates.FINISH_ORDER)
    dp.register_callback_query_handler(order_keyboard_handler.back_to_menu,
                                       lambda c: c.data and c.data.startswith('back_to_menu'),
                                       state=BotStates.FINISH_ORDER)
    dp.register_callback_query_handler(order_keyboard_handler.finish_prepay_order,
                                       lambda c: c.data and c.data.startswith('finish_prepay_order'),
                                       state=BotStates.PROCESS_PREPAY_ORDER)
    dp.register_callback_query_handler(order_keyboard_handler.back_to_menu,
                                       lambda c: c.data and c.data.startswith('back_to_menu'),
                                       state=BotStates.PROCESS_PREPAY_ORDER)

    dp.register_callback_query_handler(order_keyboard_handler.return_to_cash,
                                       lambda c: c.data and c.data.startswith('return_to_cash'),
                                       state=BotStates.WAIT_PAYMENT)


# Регистрация команд в боте
async def set_commands(ent_bot):
    commands = [
        BotCommand(command='/start', description=MessagesElements.START),
        BotCommand(command='/admin', description=MessagesElements.ADMIN)
    ]

    await ent_bot.set_my_commands(commands)


# Запуск бота
async def main():
    # logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    # register bot handlers
    register_handlers(dp)
    # register bot commands
    await set_commands(bot)
    # start bot
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
