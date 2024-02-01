#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test."""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Tests for creating a user."""

    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests for logging in a user with a wrong password."""

    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests for logging in."""

    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Tests for retrieving user information whilst logged out.
    """

    url = "{}/profile".format(BASE_URL)
    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests for retrieving profile information whilst logged in.
    """

    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    response = requests.get(url, cookies=req_cookies)
    assert response.status_code == 200

    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Tests for logging a session out.
    """

    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    response = requests.delete(url, cookies=req_cookies)
    assert response.status_code == 200

    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests for a password reset.
    """

    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "responseet_token" in response.json()

    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests for updating a user's password.
    """

    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    response = requests.put(url, data=body)
    assert response.status_code == 200

    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
