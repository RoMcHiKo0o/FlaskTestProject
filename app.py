from bson import json_util
from flask import Flask, request
from datetime import datetime
from crud import *
from database import db

app = Flask(__name__)


@app.route('/')
def home():
    return json_util.dumps({'message': get_cards(db)})


@app.route('/cards/')
def getCardsList():
    res = get_cards_list(db)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/')
def getCard(number):
    card = get_card_by_number(db, number)
    return json_util.dumps({"message": card})


@app.route('/cards/<number>/activate/')
def activateCard(number):
    res = activate_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/deactivate/')
def deactivateCard(number):
    res = deactivate_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/delete/', methods=["DELETE"])
def deleteCard(number):
    res = delete_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/<number>/rollback/')
def rollbackCard(number):
    res = rollback_card(db, number)
    return json_util.dumps({"message": res})


@app.route('/cards/filter')
def filterCards():
    cards = get_cards_list(db, dict(request.args))
    return json_util.dumps({"message": cards})


@app.route('/generate/', methods=['POST'])
def createCards():
    post = request.json
    print(post)
    if datetime.fromisoformat(post['start_date']) < datetime.now():
        post['card_state'] = "Not activated"
    elif datetime.fromisoformat(post['end_date']) < datetime.now():
        return json_util.dumps({'message': "End date should be earlier than now"})
    else:
        post['card_state'] = "Activated"
    if 'discount' not in post:
        post['discount'] = 2.0
    res = generate_cards(db, request.json)
    return json_util.dumps({'message': res})


@app.route('/cards/<number>/orders/')
def getCardOrders(number):
    orders = get_orders(db, number)
    return json_util.dumps({"message": orders})


@app.route('/orders/<order_id>/products/')
def getProducts(order_id):
    products = get_products(db, order_id)
    return json_util.dumps({"message": products})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
