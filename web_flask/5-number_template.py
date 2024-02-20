#!/usr/bin/python3
""" display “Hello HBNB!” """
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """C"""
    return ('C {}'.format(text.replace('_', ' ')))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """Python"""
    return ('Python {}'.format(text.replace('_', ' ')))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Number"""
    return ('{} is a number'.format(n))


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Number Template"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
