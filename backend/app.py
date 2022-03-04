from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(host="localhost", port=int(os.environ['SERVER_PORT']), debug=True)
