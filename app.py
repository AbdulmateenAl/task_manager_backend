from flask import Flask

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>I am him</h1><p>yh yh yh</p>"

@app.route('/create', methods=["POST"])
def create_task():
    conn = psycopg2.connect(user=USER,
                            password=PASSWORD,
                            host=HOST,
                            port=PORT,
                            dbname=DBNAME)
    
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS task_table(
                user_id             FOREIGN KEY,
                task_id             serial PRIMARY key,
                task_title          VARCHAR(255) NOT NULL,
                task_description    VARCHAR(255),
                created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status              BOOLEAN DEFAULT FALSE,
                due_date            DATE NOT NULL
                )""")

    cur.commit()
    print("Created table succesfully!")

    cur.close()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')