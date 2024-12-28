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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')