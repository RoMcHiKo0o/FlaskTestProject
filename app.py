from bson import json_util
from flask import Flask, request
from datetime import datetime
from crud import *
from database import db

# если при генерации карт скидка не указана, то скидка будет равна дефотному значению
DEFAULT_DISCOUNT = 1.0

app = Flask(__name__)


@app.route('/')
def home():
    """возвращает список всех карт со всеми полями"""
    return json_util.dumps({'message': get_cards(db)})


@app.route('/cards/')
def getCardsList():
    """возврашает список всех карты с полями series, number, create_date, end_date, card_state"""
    res = get_cards_list(db)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/')
def getCard(number):
    """возвращает карту по номеру"""
    card = get_card_by_number(db, number)
    return json_util.dumps({"message": card})


@app.route('/cards/<number>/activate/')
def activateCard(number):
    """активирует карту с номером number"""
    res = activate_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/deactivate/')
def deactivateCard(number):
    """деактивирует карту с номером number"""
    res = deactivate_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/delete/', methods=["DELETE"])
def deleteCard(number):
    """удалает карту с номером number и добавляет её в deleted_cards"""
    res = delete_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/rollback/')
def rollbackCard(number):
    """восстанавливает карту из deleted_cards"""
    res = rollback_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/filter')
def filterCards():
    """фильтрует карты из query parametres
        /cards/filter?from_create_date=2023-01-10T10:00:00&to_end_date=2023-03-23T10:00:00
        from - с какой даты
        to - по какую дату
        для поиска по другим полям просто field=value (number=1-0000)
    """
    cards = get_cards_list(db, dict(request.args))
    return json_util.dumps({"message": cards})


@app.route('/generate/', methods=['POST'])
def createCards():
    """генерирует карты
    пример json
    {
        "amount": 3,
        "series": "2",
        "start_date": "2023-02-19 14:17:15",
        "end_date": "2023-03-19 14:17:15"
    }
    скидка необязательный параметр
    """
    post = request.json
    print(post)
    if datetime.fromisoformat(post['start_date']) < datetime.now():
        post['card_state'] = "Not activated"
    elif datetime.fromisoformat(post['end_date']) < datetime.now():
        return json_util.dumps({'message': "End date should be earlier than now"})
    else:
        post['card_state'] = "Activated"
    if 'discount' not in post:
        post['discount'] = DEFAULT_DISCOUNT
    res = generate_cards(db, request.json)
    return json_util.dumps({'message': res})


@app.route('/cards/<number>/orders/')
def getCardOrders(number):
    """возврашает заказы карты с номером number"""
    orders = get_card_orders(db, number)
    return json_util.dumps({"message": orders})


@app.route('/cards/<number>/orders/filter')
def filterCardOrders(number):
    """фильтрует заказы карты
        /cards/1-0000/orders/filter?from_create_date=2023-01-10T10:00:00&to_end_date=2023-03-23T10:00:00
        from - с какой даты
        to - по какую дату
        для поиска по другим полям просто field=value (price=5.0)
    """
    orders = get_filtered_orders(db, number, dict(request.args))
    return json_util.dumps({"message": orders})


@app.route('/orders/<order_id>/products/')
def getProducts(order_id):
    """возвращает список товаров в заказе"""
    products = get_products(db, order_id)
    return json_util.dumps({"message": products})


@app.route('/cards/<number>/create_order/', methods=['POST'])
def createOrder(number):
    """создает заказ
    в POST запросе передается список словарей с id товара и количеством товара в заказе
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
    """
    res = create_order(db, number, request.json)
    return json_util.dumps({"message": res})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
