#!/usr/bin/env python3
"""
User resource module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """Returns a list of all User objects in JSON format."""
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """Returns a specific User object in JSON format.

    Args:
        user_id (str): The ID of the User.

    Returns:
        str: The User object in JSON format.

    Raises:
        404: If the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        current_user = request.current_user
        return jsonify(current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """Deletes a specific User object.

    Args:
        user_id (str): The ID of the User.

    Returns:
        str: An empty JSON response if the User has been correctly deleted.

    Raises:
        404: If the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """Creates a new User object.

    JSON body:
        - email
        - password
        - last_name (optional)
        - first_name (optional)

    Returns:
        str: The created User object in JSON format.

    Raises:
        400: If the new User cannot be created.
    """
    request_json = None
    error_msg = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        error_msg = "Wrong format"
    if error_msg is None and request_json.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and request_json.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = request_json.get("email")
            user.password = request_json.get("password")
            user.first_name = request_json.get("first_name")
            user.last_name = request_json.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """Updates a specific User object.

    Args:
        user_id (str): The ID of the User.

    JSON body:
        - last_name (optional)
        - first_name (optional)

    Returns:
        str: The updated User object in JSON format.

    Raises:
        404: If the User ID doesn't exist.
        400: If the User cannot be updated.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    request_json = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        return jsonify({'error': "Wrong format"}), 400
    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')
    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
