import os
import psycopg2
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
        cur.execute(f'SELECT id, "role" FROM "user" WHERE username=\'{email}\' and password=md5(\'{password}\')')
        data = cur.fetchone()
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