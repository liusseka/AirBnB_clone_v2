#!/usr/bin/python3
"""Starts a Flask Web Application"""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """Displays Hello hbnb"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """Displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    """Returns url with a C variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text='is cool'):
    """Returns url with a python variable"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def num(n):
    """Displays """
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>')
def num_template(n):
    """Displays a template if n is an integer"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
