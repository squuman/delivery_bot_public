class MessagesElements:
    GO_TO_JOB = 'Пришлите фото штрих-кода или номер заказа.'
    AUTH = 'Авторизуйтесь'
    AUTH_SUCCESS = 'Вы успешно вошли.\nМожете приступать к работе '
    AUTH_FAIL = 'Неверные введенные данные.\nПопробуйте еще раз'
    LOGOUT_SUCCESS = "Вы успешно вышли."
    LOGOUT_FAIL = 'Во время выхода что-то пошло не так'
    WRONG_DATA_TYPE = 'Неверный тип входных дынных'
    START_ORDER_SEARCH = 'Начинаю поиск заказа.'
    START_ORDERS_SEARCH = 'Начинаю поиск заказов.'
    NO_ONE_ORDER_HAD_BEEN_SCAN = 'Ни один заказ не был распознан'
    NO_ONE_ORDER_HAD_BEEN_FIND = 'Ни один заказ не был найден'
    DELIVERY_TYPE_NOT_CHOOSE = 'Тип доставки не был выбран'
    I_CANT_PROCESS_FEW_ORDERS = 'В данном случае я не могу обработать несколько заказов\n' \
                                ' Вы будете возвращены к прошлому состоянию'
    DELIVERY_TYPE_CANT_BE_PICKUP = 'Тип доставки не должен быть "Самовывоз"'
    DELIVERY_TYPE_MUST_BE_PICKUP = 'Тип доставки должен быть "Самовывоз"'
    ZERO_ORDERS = 'В работу нечего принимать'

    @staticmethod
    def ORDER_WAS_FOUND(order_number):
        return f'Заказ {order_number} найден'

    @staticmethod
    def ORDER_WASNT_FOUND(order_number):
        return f'Заказ {order_number} не найден. '

    ORDER_DATA = 'Данные о заказе:\n'
    CHOOSE_ACTION = 'Выберите действие'
    ORDER_WASNT_SCAN = 'Штрихкод не был распознан.\nПопробуйте ввести номер заказа'

    @staticmethod
    def ORDER_WASNT_IN_SHIPMENT(order_number):
        return f'Заказ {order_number} не укомплектован'

    @staticmethod
    def ORDER_WAS_IN_SHIPMENT(order_number=''):
        return f'Заказ {order_number} Укомплектован'

    # commands

    START = 'Начать работу'
    CANCEL = 'Отменить действие'
    LOGOUT = 'Выйти из бота'
    ADMIN = 'Войти в админ-панель'

    # actions

    CREATE_USER_FAIL = 'Что-то пошло не так'
    ADMIN_PANEL_PERMISSION_DENIED = 'Доступ запрещен'
    ADMIN_PANEL_PERMISSION_ACCESS = 'Вы вошли в панель админа.\nВыберите действия:'
    NEW_PASSWORD_WAS_CREATED = 'Сгенерирован новый пароль:'
    CHOOSE_USER = 'Выберите пользователя: '
    YOU_RETURN_TO_PROCESS_STATE = 'Вы вернулись в рабочее состояние'
    DELETE_USER_SUCCESS = 'Пользователь успешно удален'
    DELETE_USER_FAIL = 'Что-то пошло не так'
    USER_ALREADY_IS_ADMIN = 'Пользователь уже является админом'
    DELETE_ADMIN_SUCCESS = 'Админ успешно удален'
    DELETE_ADMIN_FAIL = 'Что-то пошло не так'
    ADD_ADMIN_SUCCESS = 'Админ успешно добавлен'
    ADD_ADMIN_FAIL = 'Что-то пошло не так'
    BACK_TO_ADMIN = 'В начало'

    # keyboards

    ADMIN_USERS_LIST = 'Список пользователей'
    ADMIN_ADD_USER = 'Добавить пользователя'
    ADMIN_DELETE_USER = 'Удалить пользователя'
    ADMIN_ADMINS_LIST = 'Список админов'
    ADMIN_ADD_ADMIN = 'Добавить админа'
    ADMIN_DELETE_ADMIN = 'Удалить админа'
    ADMIN_BACK = 'Назад'

    GET_ORDER_TO_DELIVERY = 'Забрать в доставку'
    GET_ORDER_TO_DELIVERY_BACK = '👈 Назад'
    START_TURN_ORDERS_TO_DELIVERY = 'Начинаю передачу заказов в доставку'
    TURN_ORDERS_TO_DELIVERY_FINISHED = 'Передача заказов в доставку завершена'

    @staticmethod
    def ORDER_WAS_TURN_TO_DELIVERY(order_number):
        return f'ОК! Заказ {order_number} передан в доставку.'

    @staticmethod
    def ORDER_WASNT_TURN_TO_DELIVERY(order_number):
        return f'Заказ {order_number} не был передан в доставку. :('

    PICKUP_GIVE = 'Выдать заказ'
    PICKUP_BACK = 'Назад'
    CLOSE_ORDER = 'Закрыть заказ'
    ORDER_WAS_CLOSED = 'Заказ закрыт'

    @staticmethod
    def ORDER_PAYMENT_AMOUNT(amount):
        if len(str(amount)) > 1:
            amount = "{:,}".format(amount)
            amount = str(amount).replace(',', ' ')
            amount = str(amount).replace('.', ',')
            amount_array = amount.split(',')
            if len(amount_array[len(amount_array) - 1]) == 1:
                amount += '0'

        return f'К оплате *{amount} ₽*.'

    CHOOSE_PAYMENT_METHOD = 'Выберите способ оплаты:'
    CASH = 'Наличными'
    LINK = 'По ссылке'
    FINISH_ORDER = 'Завершить заказ'

    @staticmethod
    def ORDER_WAS_FINISHED(number):
        return f'ОК! Заказ {number} завершен.'

    @staticmethod
    def ORDER_WASNT_FINISHED(number):
        return f'Заказ {number} не был завершен'

    PAYMENT_WAS_CREATED = 'Оплата была создана'
    PAYMENT_WASNT_CREATED = 'Оплата не была создана, вы будете возвращены к рабочему состоянию'
    PAYMENT_LINK_WAS_CREATED = 'Ссылка на оплату была сформирована'
    PAYMENT_LINK_WASNT_CREATED = 'Ссылка на оплату не была сформирована, вы будете возвращены к рабочему состоянию'
    PAYMENT_LINK_WAS_PASS_TO_ORDER = 'Ссылка на оплату была отправлена покупателю в СМС-сообщении ' \
                                     'и по электронной почте.'
    PAYMENT_LINK_WASNT_PASS_TO_ORDER = 'Ссылка на оплату не была передана в заказ'
    WAIT_PAYMENT = 'Ожидается оплата.'
    WAIT_PAYMENT_TIMEOUT = 'Время ожидания оплаты заказа истекло. Вы будете возвращены к исходному состоянию'
    ORDER_WAS_PAID = 'Заказ оплачен'

    @staticmethod
    def ORDER_WAS_PAID_AND_FINISHED(number):
        return f'ОК! Заказ {number} успешно оплачен и завершен.'

    ORDER_WASNT_PAID = 'Заказ не оплачен'
    PAYMENT_NOT_NEED = 'Оплата не требуется.'
    PREPAY_FLAG_IS_TRUE = 'В заказа проставлена постоплата'
    CHECK_PAYMENT = 'Проверить оплату'

    CASH_PAYMENT_WAS_CHOOSED = 'Выбрана оплата наличными. Завершить заказ?'
    FOR_SHIPMENT = '[Укомплектован].'
    READY_TO_SHIPMENT = '[Готов к самовывозу].'
    SEND_TO_DELIVERY = '[Передан в доставку].'

    TO_START = '👈 В начало'
    FINISH = 'Завершить'

    RETURN_TO_CASH = '👈 Вернуться к наличным'

    SOMETHING_WRONG = 'Что-то не так'
