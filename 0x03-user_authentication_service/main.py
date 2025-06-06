import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)

    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}"
    assert response.json() == {
        "email": email, "message": "user created"}, f"Unexpected payload: {
        response.json()}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Tries to log in with a wrong password."""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)

    assert response.status_code == 401, f"Expected 401, got {
        response.status_code}"


def log_in(email: str, password: str) -> str:
    """log in"""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)

    assert response.status_code == 200, f"Expected 401, got {
        response.status_code}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """profile without session id"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, f"Expected 403, got {
        response.status_code}"


def profile_logged(session_id: str) -> None:
    """profile with session id"""
    url = f"{BASE_URL}/profile"
    payload = {"session_id": session_id}
    response = requests.get(url, cookies=payload)
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}"


def log_out(session_id: str) -> None:
    """logout with session id"""
    url = f"{BASE_URL}/sessions"
    payload = {"session_id": session_id}
    response = requests.delete(url, cookies=payload)
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}"


def reset_password_token(email: str) -> str:
    """reset password tokken"""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}"
    reset_token = response.json()
    return reset_token.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    url = f"{BASE_URL}/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(url, data=payload)
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
