from flask import Flask
import os
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 app.py <ip> <port>")
        
    ip = sys.argv[1]
    port = int(sys.argv[2])

    app.run(host=ip, port=port)

if __name__ == '__main__':
    main()
