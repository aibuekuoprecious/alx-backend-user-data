#!/usr/bin/env python3
"""
This is the main module for the API.
"""

from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

# Check the AUTH_TYPE and initialize the appropriate authentication object
if AUTH_TYPE == 'auth':
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()


@app.before_request
def before_request():
    """
    Before request handler.
    """
    if auth is not None:
        excluded_list = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if auth.require_auth(request.path, excluded_list):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found error handler.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized error handler.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden error handler.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
