from functools import wraps
from flask import abort
from flask_login import current_user
from uuid import UUID
from flask import jsonify
from base64 import b64decode


def teacher_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.type == "student":
            return jsonify({"message": "Access denied"}), 403
        return func(*args, **kwargs)
    return decorated_view

def student_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.type == "teacher":
            return jsonify({"message": "Access denied"}), 403
        return func(*args, **kwargs)
    return decorated_view


def validate_id(value: UUID):
    return isinstance(value, UUID)


def is_base64(s):
    try:
        b64decode(s)
        return True
    except Exception:
        return False