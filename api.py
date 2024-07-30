import json
from flask import Flask, jsonify, request
from helpers import login, encrypt_bearer_token
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


@app.route('/')
def helloWorld():
    return "<p>Hello, World!</p>"


@app.route('/login', methods=['POST'])
def login_ep():
    response = app.make_default_options_response()
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'

    data = {'success': True, 'id_user': None, 'bearer_token': None}
    try:
        body = request.get_json()
        user = login(body['email'], body['password'])
        if user != None:
            data['id_user'] = user[0]
            data['bearer_token'] = encrypt_bearer_token(data['id_user'])
    except Exception as e:
        data['success'] = False
        print(str(e))
    return jsonify(data)