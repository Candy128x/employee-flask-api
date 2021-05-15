from flask import Flask
from helper.db_helper import DbHelper

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def home():
    return 'Hello Developer :]'


@app.route('/employee/create', methods=['POST'])
def home():
    return 'Hello Developer :]'


if __name__ == '__main__':
    app.run()