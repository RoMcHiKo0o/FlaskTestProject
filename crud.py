def serialize(doc):
    for i, j in doc:
        print(i, j)
    return [{**i, "_id": str(i["_id"])} for i in doc]


def get_cards(db):
    return [i for i in db.cards.find()]


def get_card_by_id(db, id):
    pass


def update_card(db, id, newcard):
    pass
