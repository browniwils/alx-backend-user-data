#!/usr/bin/env python3
"""Module of Index views.
"""
from flask import jsonify
from flask import abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET status of the API always OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET number of each objects."""
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """GET Unauthorized error."""

    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Forbidden error."""
    abort(403)
