#!/usr/bin/env python3
"""Views of api module."""

from flask import abort
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET status of the API."""

    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET number of objects."""

    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Unauthorized error."""

    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Forbidden error."""

    abort(403)
