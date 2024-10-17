from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>I am him</h1><p>yh yh yh</p>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')