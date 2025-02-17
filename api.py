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
        user_data = login(body['email'], body['password'])
        if user_data != None:
            data['id_user'] = user_data[0][0]
            data['role'] = user_data[0][1] 
            data['bearer_token'] = encrypt_bearer_token(data['id_user'])
            data['cummulus'] = []
            for ud_item in user_data:
                if ud_item[2] != None:
                    data['cummulus'].append(ud_item[2])
    except Exception as e:
        data['success'] = False
        print(str(e))
    return jsonify(data)
