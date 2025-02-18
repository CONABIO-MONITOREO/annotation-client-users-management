import json
from flask import Flask, jsonify, request
from helpers import login, encrypt_bearer_token, get_users_h, validate_bearer_token, create_user_h, update_user_h
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


@app.route('/users', methods=['GET'])
def get_users():
    user_id = validate_bearer_token(request.headers)
    response = app.make_default_options_response()
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    data = []
    try:
        data = get_users_h()
    except Exception as e:
        print(str(e))
    return jsonify({'data':data, 'success': True})


@app.route('/user', methods=['POST'])
def create_user():
    user_id = validate_bearer_token(request.headers)
    response = app.make_default_options_response()
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    data = []
    data = {'success': True, 'id_user': None}
    try:
        body = request.get_json()
        user = create_user_h(body['email'], body['password'], body['role'], body['cummulus_name'])
        data['id_user'] = user['id']
    except Exception as e:
        print(str(e))
    return jsonify(data)


@app.route('/user', methods=['PUT'])
def update_user():
    user_id = validate_bearer_token(request.headers)
    response = app.make_default_options_response()
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    data = []
    data = {'success': True, 'id_user': None}
    try:
        body = request.get_json()
        user = update_user_h(body['user_id'])
        data['id_user'] = user['id']
    except Exception as e:
        print(str(e))
    return jsonify(data)
