import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import cryptocode
import json
from datetime import datetime, timedelta

load_dotenv()

dbname = os.getenv('POSTGRES_DB')
dbuser = os.getenv('POSTGRES_USER')
dbpass = os.getenv('POSTGRES_PASSWORD')
dbhost = os.getenv('POSTGRES_HOST')
dbport = os.getenv('POSTGRES_PORT')
jwtkey = os.getenv('JWTKEY')

conn = psycopg2.connect(f'dbname={dbname} user={dbuser} \
                        password={dbpass} host={dbhost} port={dbport}')


def login(email, password):
    data = None
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT u.id, "role", cm.cummulus_name FROM "user" as u LEFT JOIN cummulus_relation as cm ON u.id=cm.user_id WHERE username=\'{email}\' and password=md5(\'{password}\') and u.is_active')
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
    return data


def encrypt_bearer_token(id_user):
    current_datetime = datetime.now()
    current_datetime = current_datetime + timedelta(days=1)
    current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    data = {'id_user': id_user, 'ends_at': current_datetime}
    string_data = json.dumps(data)
    bearer_token = cryptocode.encrypt(string_data, jwtkey)
    return bearer_token


def get_users_h():
    data = None
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f'SELECT u.id, u.username as email, u."role", u.is_active, cm.cummulus_name as cummulus FROM "user" as u LEFT JOIN cummulus_relation as cm ON u.id=cm.user_id')
        data = cur.fetchall()
        data = [dict(d) for d in data]
        cur.close()
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
    return data


def validate_bearer_token(headers):
    try:
        bearer_token = headers['Authorization'].split(' ')[1]
        string_data = cryptocode.decrypt(bearer_token, jwtkey)
        data = json.loads(string_data)
        ends_at = datetime.strptime(data['ends_at'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > ends_at:
            print('jwt expirado')
        return  data['id_user']
    except Exception as e:
        print('Error al validar el jwt', str(e))
    return None


def create_user_h(email, password, role, cummulus):
    data = None
    try:
        cur = conn.cursor()
        sql = f'INSERT INTO "user"(username, password, role) VALUES(\'{email}\', md5(\'{password}\'), \'{role}\') RETURNING id'
        cur.execute(sql)
        data = cur.fetchone()
        if cummulus != None:
            sql = f"INSERT INTO cummulus_relation(cummulus_name, user_id) VALUES('{cummulus}', {data[0]})"
            cur.execute(sql)
        cur.close()
        conn.commit()
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
    return data


def update_user_h(user_id):
    data = {'user_id': None}
    try:
        cur = conn.cursor()
        sql = f'UPDATE "user" SET is_active=not is_active WHERE id = {user_id}'
        cur.execute(sql)
        cur.close()
        conn.commit()
        data['user_id'] = user_id
    except Exception as e:
        print(str(e))
    finally:
        cur.close()
    return data