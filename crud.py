from copy import copy
from datetime import datetime
from datetime import timedelta

from bson import ObjectId
# поля которые выводятся по умолчанию
DEFAULT_FIELDS = {'_id': 0, 'series': 1, 'number': 1, 'create_date': 1, 'end_date': 1, 'card_state': 1}


def convert_card_type(field):
    """возвращает тип для поля карты (None если приведение типов не требуется)"""
    if field in ['number', 'series', 'card_state']:
        return str
    if field == 'discount':
        return float
    if field == 'buy_counter':
        return int
    return None


def convert_order_type(field):
    """возвращает тип для поля заказа (None если приведение типов не требуется)"""
    if field in ['discount', 'total', 'price']:
        return float
    if field == "amount":
        return int
    return None


def generate_number(n):
    """генерирует следующий номер карты
        generate_number('1-0031') -> '1-0032'
    """
    return f"{n[:2]}{int(n[2:]) + 1:04}"


def get_cards(db):
    """возвращает все карты со всеми полями кроме _id"""
    return [i for i in db.cards.find({}, {'_id': 0})]


def get_cards_list(db, filter_search=None, fields=None):
    """возврашает список карт с учетом фильтров и проекции
        fields cловарь вида {field1: 1 либо 0, field2: 1 либо 0, ...}
        filter_search словарь фильтров как в mongodb, например {field1: value1, field2: value2}
        фильтр дат из query параметров переводится в фильтрацию из mongodb
        from - с какой даты
        to - по какую дату
    """
    if fields is None:
        fields = DEFAULT_FIELDS

    if filter_search is None:
        filter_search = {}
    else:
        for k, v in tuple(filter_search.items()):
            if k == 'from_create_date':
                filter_search['create_date'] = {"$gte": datetime.fromisoformat(v)}
                filter_search.pop('from_create_date')
            if k == 'to_create_date':
                filter_search['create_date'] = {"$lte": datetime.fromisoformat(v)}
                filter_search.pop('to_create_date')
            if k == 'from_end_date':
                filter_search['end_date'] = {"$gte": datetime.fromisoformat(v)}
                filter_search.pop('from_end_date')
            if k == 'to_end_date':
                filter_search['end_date'] = {"$lte": datetime.fromisoformat(v)}
                filter_search.pop('to_end_date')
            elif (tpe := convert_card_type(k)) is not None:
                filter_search[k] = tpe(v)
    return [i for i in db.cards.find(filter_search, fields)]


def get_card_by_number(db, number):
    """возвращает карту по номеру. {} если карты с таким номером нет"""
    return next(db.cards.find({'number': number}), {})


def get_card_state(db, number):
    """возвращает состояние карты"""
    card = db.cards.find({'number': number}, {"_id": 0, 'card_state': 1})
    return list(card)[0]['card_state']


def activate_card(db, number):
    """активирует карту по номеру. Если карта уже активирована, либо просрочена, то возвращает соотвествующее
    сообщение"""
    state = get_card_state(db, number)
    if state == "Not activated":
        db.cards.update_one({'number': number}, {'$set': {
            'card_state': "Activated",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=30),
        }})
        return "Card was successfully activated"
    elif state == "Expired":
        return 'Card is expired'
    else:
        return 'Card is already activated'


def deactivate_card(db, number):
    """деактивирует карту по номеру. Если карта уже не активна, либо просрочена, то возвращает соотвествующее
        сообщение"""
    state = get_card_state(db, number)
    if state == "Activated":
        db.cards.update_one({'number': number}, {'$set': {
            'card_state': "Not activated",
            "start_date": '',
            "end_date": '',
        }})
        return "Card was successfully deactivated"
    elif state == "Expired":
        return 'Card is expired'
    else:
        return 'Card is not activated'


def delete_card(db, number):
    """удаляет карту по номеру и добавляет её в deleted_cards. Если возникает ошибка выводится соответствующее
    сообщение"""
    card = get_card_by_number(db, number)
    if card == {}:
        return 'No card with that number'
    db.deleted_cards.insert_one(card)
    db.cards.delete_one({"number": number})
    return "card was deleted"


def get_deleted_card_by_number(db, number):
    """возвращает карту из deleted_cards по номеру, если карты нет, то возвращает {}"""
    return next(db.deleted_cards.find({'number': number}), {})


def rollback_card(db, number):
    """восстанавливает карту по номеру. При возникновении ошибок возвращает соответствующую ошибку"""
    card = get_deleted_card_by_number(db, number)
    if card == {}:
        return 'There is no deleted card with that number'
    res = insert_deleted_card(db, card)
    if card == res:
        db.deleted_cards.delete_one({"number": card['number']})
        return "card was restored"
    else:
        return res


def insert_deleted_card(db, card):
    """добавляет карту в delered_cards. Если такая карта уже есть, то возвращает ошибку"""
    filter_search = {"$or": [{"_id": card['_id']}, {'series': card['series'], 'number': card['number']}]}
    res = get_cards_list(db, filter_search=filter_search)
    if not res:
        db.cards.insert_one(card)
        return card
    else:
        return "Card already exists"


def generate_cards(db, json):
    """генерирует карты по json объекту с полями
    'series', 'discount', 'create_date', 'start_date', 'end_date', 'card_state'
    """
    tmp = get_cards_list(db, filter_search={'series': json['series']}, fields={"_id": 0, "number": 1})
    number = f"{json['series']}-0000"
    last_number = 0
    if len(tmp) != 0:
        last_number = max([i['number'] for i in tmp])
    for i in range(json['amount']):
        if last_number != 0:
            number = generate_number(last_number)
        last_number = number
        card = {
            "series": json['series'],
            "number": number,
            "orders": [],
            "buy_counter": 0,
            "recent_buy_date": '',
            "discount": json['discount'],
            "create_date": datetime.now(),
            "start_date": json['start_date'],
            "end_date": json['end_date'],
            'card_state': json['card_state']
        }
        db.cards.insert_one(card)
    return "Cards have been added"


def get_order_by_id(db, order_id):
    """возвращает заказ по id"""
    if not isinstance(order_id, ObjectId):
        order_id = ObjectId(order_id)
    return next(db.orders.find({"_id": order_id}, {"_id": 0}), {})


def get_card_orders(db, number):
    """возвращает заказы карты"""
    return get_filtered_orders(db, number)


def get_filtered_orders(db, number, filter_search=None):
    """возвращает заказы карты после фильтрации
        filter_search словарь фильтров как в mongodb, например {field1: value1, field2: value2}
        фильтр дат из query параметров переводится в фильтрацию из mongodb
        from - с какой даты
        to - по какую дату
    """
    if filter_search is None:
        filter_search = {}
    else:
        for k, v in tuple(filter_search.items()):
            if k == 'from_date':
                filter_search['date'] = {"$gte": datetime.fromisoformat(v)}
                filter_search.pop('from_date')
            if k == 'to_date':
                filter_search['date'] = {"$lte": datetime.fromisoformat(v)}
                filter_search.pop('to_date')
            elif (tpe := convert_order_type(k)) is not None:
                filter_search[k] = tpe(v)
    filter_search['card_number'] = number
    print(filter_search)
    return list(db.orders.find(filter_search))


def get_product_by_id(db, prod_id, fields=None):
    """возвращает товар по id"""
    if fields is None:
        fields = {}
    if not isinstance(prod_id, ObjectId):
        prod_id = ObjectId(prod_id)
    return next(db.products.find({"_id": prod_id}, fields), {})


def get_products(db, order_id):
    """возврашает товары заказа"""
    order = get_order_by_id(db, order_id)
    if order == {}:
        return "No order with that id"
    prod_list = order['products']
    return [{**get_product_by_id(db, prod['id'], {"_id": 0, "name": 1}), "amount": prod['amount']} for prod in
            prod_list]


def add_card_order(db, number, order_id):
    """добавляет заказ в список поле orders карты с номером number"""
    db.cards.update_one(
        {"number": number},
        {
            "$push": {"orders": ObjectId(order_id)},
            "$inc": {"buy_counter": 1},
            "$set": {"recent_buy_date": datetime.now()}
        }
    )


def create_order(db, number, json):
    """создает заказ для карты с номером number по json объекту
    [{товар1, количество1},{товар2, количество2}, ...]
    пример json:
    [
    {
        "id": "63ef4839a6a36ecd62717f02",
        "amount": 1
    },
    {
        "id": "63ef4839a6a36ecd62717f03",
        "amount": 3
    }
    ]
    При возникновении ошибки выдается соответствующая ошибка
    """
    card = get_card_by_number(db, number)
    if card == {}:
        return "No card with that number"
    if card['card_state'] != 'Activated':
        return "Card must be activated"
    discount = card['discount']
    products = []
    price = 0
    for el in json:
        if el['amount'] <= 0 and isinstance(el['amount'], int):
            return "Amount must be positive and integer"
        prod = get_product_by_id(db, el['id'], {"_id": 0, "price": 1})
        if prod == {}:
            return "No product with that id"
        price += prod['price'] * el['amount']
        products.append(
            {
                "id": ObjectId(el['id']),
                "amount": int(el['amount'])
            }
        )
        if not products:
            return "Empty order"

    order = {
        "card_number": number,
        "date": datetime.now(),
        "price": price,
        "discount": discount,
        "total": price * (100 - discount) / 100,
        "products": products
    }
    order_id = db.orders.insert_one(order).inserted_id
    add_card_order(db, number, order_id)
    return "Order was successfully created"
