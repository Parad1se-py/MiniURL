from flask import session, abort

def login_is_required(function):
    def wrapper(*args, **kwargs):
        return abort(401) if "google_id" not in session else function
    return wrapper