from flask import Flask, request
import os
import sys
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/method1")
def generate_regex_visualization_method1():
    regex_str = request.args['str']
    base64arr = None
    with open("test_img.png", 'rb') as f:
        byte_arr = f.read()   
        base64arr = base64.standard_b64encode(byte_arr)
    return base64arr

def main():
    if len(sys.argv) != 3:
        print("Error, usage: python app.py <ip> <port>")

    ip = sys.argv[1]
    port = int(sys.argv[2])

    app.run(host=ip, port=port)

if __name__ == '__main__':
    main()
