from flask import Flask, jsonify, request, g
from flask_cors import CORS
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)
CORS(app)

import os
from dotenv import load_dotenv
load_dotenv()
password = os.getenv('haslo')

def create_connection():
    try:
        connection = psycopg2.connect(
            host='central',
            user='postgres',
            password=password,
            database='cwl1'
        )
        print("Połączenie z bazą danych PostgreSQL udane")
        return connection
    except OperationalError as e:
        print(f"Błąd połączenia z bazą danych: '{e}'")
        return None

def fetch_all_dogs(cursor):
    cursor.execute("SELECT * FROM dogs")
    columns = []
    for desc in cursor.description:
        columns.append(desc[0])
    result = []
    for row in cursor.fetchall():
        print(row)
        row_dict = {}
        for col, val in zip(columns, row):
            row_dict[col] = val
        result.append(row_dict)
    print(result)
    return result

def insert_dog(cursor, dog_data):
    query = """
    INSERT INTO dogs (name, race, color, photo, number, illnesses)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (dog_data['name'], dog_data['race'], dog_data['color'],
                           dog_data['photo'], dog_data['number'], dog_data['illnesses']))

def delete_dog(cursor, dog_id):
    query = "DELETE FROM dogs WHERE id = %s"
    cursor.execute(query, (dog_id,))

@app.before_request
def before_request():
    g.connection = create_connection()

@app.teardown_request
def teardown_request(exception):
    connection = getattr(g, 'connection', None)
    if connection:
        connection.close()

@app.route('/')
def home():
    return "Witamy w API Schroniska dla Psów!"

@app.route('/api/dogs', methods=['GET'])
def get_dogs():
    cursor = g.connection.cursor()
    dogs = fetch_all_dogs(cursor)
    cursor.close()
    return jsonify(dogs)

@app.route('/api/dogs/addDog', methods=['POST'])
def post_dog():
    new_dog = request.get_json()
    cursor = g.connection.cursor()
    insert_dog(cursor, new_dog)
    g.connection.commit()
    cursor.close()
    return jsonify({"message": "Pies dodany pomyślnie!"}), 201

@app.route('/api/dogs/delete', methods=['POST'])
def remove_dog():
    info = request.get_json()
    delete_dog(info['id'])

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)