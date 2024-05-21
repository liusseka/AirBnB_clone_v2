#!/usr/bin/python3
"""Starts a Flask Web Application"""

from flask import Flask
app.url_map.strict_slashes = False

app = Flask(__name__)


@app.route('/')
def hello_hbnb:
    """Displays Hello hbnb"""
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
