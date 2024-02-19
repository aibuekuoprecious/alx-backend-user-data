#!/usr/bin/env python3
"""Module for Index views"""

from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """Handle unauthorized access"""
    abort(401, description='Unauthorized')


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """Handle forbidden access"""
    abort(403, description='Forbidden')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Get the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Get the number of each object"""
    stats = {
        'users': User.count()
    }
    return jsonify(stats)
