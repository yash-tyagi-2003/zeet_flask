from flask import Flask, request, jsonify
import main
from flask_cors import CORS
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
