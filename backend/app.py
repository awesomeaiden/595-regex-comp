## Standard Python Imports
import sys
import base64
import json

## Imported Package Imports
from flask import Flask, request, Response, send_from_directory

## Project Imports

app = Flask(__name__, static_folder='test_pages/')



@app.route("/method1", methods=['POST'])
def generate_regex_visualization_method1():
    regex_str = request.args['str']
    base64arr = None
    with open("../test_img.png", 'rb') as f:
        byte_arr = f.read()
        base64arr = base64.standard_b64encode(byte_arr)
    return base64arr

@app.route("/<path:path>")
def main_serve(path):
    return send_from_directory('npm_build/', path)

def main():
    if len(sys.argv) != 3:
        print("Error, usage: python app.py <ip> <port>")
        exit()

    ip = sys.argv[1]
    port = int(sys.argv[2])

    app.run(host=ip, port=port)


if __name__ == '__main__':
    main()
