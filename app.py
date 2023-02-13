from flask import Flask
from database import db

app = Flask(__name__)


@app.route('/')
def home():
    print(db)
    return '6887'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
