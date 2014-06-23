# coding: utf-8

from functools import wraps
from google.appengine.api import users
from flask import redirect, abort


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(403)  # Unauthorized
            return func(*args, **kwargs)
        return redirect('/login/required/')
    return view
