#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
import os
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

auth_type = os.getenv('AUTH_TYPE')
if auth_type == 'basic_auth':
    auth = BasicAuth()  # instance of BasicAuth
else:
    auth = Auth()


@app.before_request
def before_request() -> str:
    """ Filter each request based on authentication. """
    if auth is None:
        return

    # paths that are not subject to authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Authentication Requirement Check
    if not (auth.require_auth(request.path, excluded_paths)):
        return

    # Authorization Header Check
    if (auth.authorization_header(request)) is None:
        abort(401)

    # Current User Check
    if (auth.current_user(request)) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handle Unauthorized error (401)."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Handle Forbidden error (403)."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handle Not found error (404).   """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
