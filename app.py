import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies


import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('SECRETKEY')
jwt = JWTManager(app)

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")



def connect_to_db():

    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

@app.route('/register', methods=['GET', 'POST'])
def register():

    # Checking the type of data we are receiving so we can handle it properly
    if request.content_type == 'application/json':
        response = request.get_json() #For json
    else:
        response = request.form #For form

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS users(
                    id          PRIMARY KEY
                    name        VARCHAR(255)
                    password    VARCHAR(255)
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
                    )
        cur.execute("""
                        INSERT INTO users (name, password) VALUES (%s, %s);""",
                        (response.get('user'), response.get('password')))
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": f"User {response.get('user')} created successfully"})


@app.route('/')
def home():
    return "<h1>I am him</h1><p>yh yh yh</p>"


@app.route('/task', methods=["POST"])
def create_task():  # Create tasks

    # Checking the type of data we are receiving so we can handle it properly
    if request.content_type == 'application/json':
        response = request.get_json()  # For json
    else:
        response = request.form  # For form

    conn = connect_to_db()  # Connect to the supabase database

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
                user_id             FOREIGN KEY,
                task_id             SERIAL PRIMARY key,
                title          VARCHAR(255) NOT NULL,
                description    VARCHAR(255),
                created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status              BOOLEAN DEFAULT FALSE,
                due_date            DATE NOT NULL
                )""")  # Create a tasks table in the database if it doesn't exist
    cur.execute("""
                    INSERT INTO tasks (task_id, title, description, created_at, status, due_date) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (response.get('task_id'), response.get('title'), response.get('description'), response.get('created_at'), response.get('status'), response.get('due_date'))
                    ) # Inserts the items into database

    cur.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Created task successfully!"})


@app.route('/tasks', methods=['GET'])
def get_tasks():

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
                        SELECT task_id, title, description, status, created_at, due_date FROM tasks
                    """)  # Selects some specific data to be displayed might create INDEX later
    except Exception as e:
        return jsonify({"message": str(e)})

    return jsonify({"message": "Tasks fetch successfully"})


@app.route('/task/<int:id>', methods=['GET'])
def get_a_task(id):

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
                        SELECT task_id, title, description, status, created_at, due_date FROM tasks WHERE task_id = %s,""" (id,)
                    )
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": f"TaskID {id} has been fetched"})

@app.route('/task/<int:id>', methods=['PUT'])
def update_task(id):

    if request.content_type == 'application/json':
        response = request.get_json()
    else:
        response = request.form

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
                        UPDATE tasks SET title = %s, description = %s, status = %s, due_date = %s WHERE task_id = %s""",
                        (response.get('title'), response.get('description'), response.get('status'), response.get('due_date'), id)
                        )
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": "Updated task successfully"})

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
                        DELETE FROM tasks WHERE task_id = %s""", (id,))
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"message": str(e)})
    
    return jsonify({"message": f"Deleted taskID {id} successfully"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
