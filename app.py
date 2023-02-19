from flask import Flask, request
from crud import *
from database import db
from bson import json_util

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
