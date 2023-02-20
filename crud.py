from datetime import datetime
from datetime import timedelta

from bson import ObjectId

DEFAULT_FIELDS = {'_id': 0, 'series': 1, 'number': 1, 'create_date': 1, 'end_date': 1, 'card_state': 1}


def convert_type(field):
    if field in ['number', 'series', 'card_state']:
        return str
    if field == 'discount':
        return float
    if field == 'buy_counter':
        return int
    return None


def generate_number(n):
    return f"{n[:2]}{int(n[2:]) + 1:04}"


def get_cards(db):
    return [i for i in db.cards.find({}, {'_id': 0})]


def get_cards_list(db, filter_search=None, fields=None):
    if fields is None:
        fields = DEFAULT_FIELDS

    if filter_search is None:
        fields = {}
    else:
        for k, v in filter_search.items():
            if (tpe := convert_type(k)) is not None:
                filter_search[k] = tpe(v)
    return [i for i in db.cards.find(filter_search, fields)]


def get_card_by_number(db, number):
    return next(db.cards.find({'number': number}), {})


def get_card_state(db, number):
    card = db.cards.find({'number': number}, {"_id": 0, 'card_state': 1})
    return list(card)[0]['card_state']


def activate_card(db, number):
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
    card = get_card_by_number(db, number)
    if card == {}:
        return 'No card with that number'
    db.deleted_cards.insert_one(card)
    db.cards.delete_one({"number": number})
    return "card was deleted"


def get_deleted_card_by_number(db, number):
    return next(db.deleted_cards.find({'number': number}), {})


def rollback_card(db, number):
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
    filter_search = {"$or": [{"_id": card['_id']}, {'series': card['series'], 'number': card['number']}]}
    res = get_cards_list(db, filter_search=filter_search)
    if not res:
        db.cards.insert_one(card)
        return card
    else:
        return "Card already exists"


def generate_cards(db, json):
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
            "discount": json['discount'],
            "create_date": datetime.now(),
            "start_date": json['start_date'],
            "end_date": json['end_date'],
            'card_state': json['card_state']
        }
        db.cards.insert_one(card)
    return "Cards have been added"


def get_order_by_id(db, order_id):
    if not isinstance(order_id, ObjectId):
        order_id = ObjectId(order_id)
    return next(db.orders.find({"_id": order_id}, {"_id": 0}), {})


def get_orders(db, number):
    order_list = get_card_by_number(db, number)['orders']
    return [get_order_by_id(db, order) for order in order_list]


def get_product_by_id(db, prod_id, fields=None):
    if fields is None:
        fields = {}
    if not isinstance(prod_id, ObjectId):
        prod_id = ObjectId(prod_id)
    return next(db.products.find({"_id": prod_id}, fields), {})


def get_products(db, order_id):
    order = get_order_by_id(db, order_id)
    if order == {}:
        return "No order with that id"
    prod_list = order['products']
    return [{**get_product_by_id(db, prod['id'], {"_id": 0, "name": 1}), "amount": prod['amount']} for prod in prod_list]
