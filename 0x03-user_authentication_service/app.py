#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    """ Returns a JSON response with a welcome message. """
    return (jsonify({"message": "Bienvenue"}), 200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
