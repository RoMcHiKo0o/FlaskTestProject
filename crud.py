DEFAULT_FIELDS = {'_id': 0, 'series': 1, 'number': 1, 'create_date': 1, 'end_date': 1, 'card_state': 1}


def convert_type(field):
    if field in ['number', 'series', 'card_state']:
        return str
    if field == 'discount':
        return float
    if field == 'buy_counter':
        return int
    return None


def get_cards(db):
    return [i for i in db.cards.find({}, {'_id': 0})]


def get_cards_list(db, filter_search=None, fields=None):
    if fields is None:
        fields = DEFAULT_FIELDS
    if filter_search is None:
        fields = {}
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
        db.cards.update_one({'number': number}, {'$set': {'card_state': "Activated"}})
        return "Card was successfully activated"
    elif state == "Expired":
        return 'Card is expired'
    else:
        return 'Card is already activated'


def deactivate_card(db, number):
    state = get_card_state(db, number)
    if state == "Activated":
        db.cards.update_one({'number': number}, {'$set': {'card_state': "Not activated"}})
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
