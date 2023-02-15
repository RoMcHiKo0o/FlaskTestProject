def serialize(doc):
    return [{**i, "_id": str(i["_id"])} for i in doc]


def get_cards(db):
    return serialize(db.cards.find())
