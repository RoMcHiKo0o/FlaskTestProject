from flask import Flask
from crud import *
from database import db
from bson.json_util import dumps

app = Flask(__name__)


@app.route('/')
def home():
    return get_cards(db)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
