#!/usr/bin/env python3
"""session authenticating api views."""

import os
from typing import Tuple
from flask import abort
from flask import jsonify
from flask import request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST JSON representation of a User object."""

    res_not_found = {"error": "no user found for this email"}
    email = request.form.get("email")

    if email is None or len(email.strip()) == 0 or "@" not in email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify(res_not_found), 404
    if len(users) <= 0:
        return jsonify(res_not_found), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        response = jsonify(users[0].to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return response
    return jsonify({"error": "wrong password"}), 401

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE object."""

    from api.v1.app import auth
    deleted = auth.destroy_session(request)
    if not deleted:
        abort(404)
    return jsonify({})
