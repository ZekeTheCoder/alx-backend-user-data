#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

# Create an instance of the Flask application
app = Flask(__name__)

# Configure the Flask application to pretty-print JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register the Blueprint for API views
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for the API routes
# This allows requests from any origin (useful for development)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the authentication variable
auth = None

# Get the authentication type from environment variables
auth_type = getenv('AUTH_TYPE')

# Select the authentication method based on the environment variable
if auth_type == 'basic_auth':
    auth = BasicAuth()  # instance of BasicAuth
elif auth_type == "session_auth":
    auth = SessionAuth()  # instance of SessionAuth
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()  # instance of SessionExpAuth
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()  # instance of SessionDBAuth
else:
    auth = Auth()  # Default Auth


@app.before_request
def before_request() -> str:
    """ Filter each request based on authentication. """
    if auth is None:
        return

    # paths that are not subject to authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    # Authentication Requirement Check
    if not (auth.require_auth(request.path, excluded_paths)):
        return

    # Set the current user
    request.current_user = auth.current_user(request)

    # Authorization Header or Session Cookie Check
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    # Current User Check
    if request.current_user is None:
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
    app.run(host=host, port=port, debug=True)
