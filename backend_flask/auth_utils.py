from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request


ALLOWED_ROLES = {"job_seeker", "employer", "admin"}


def normalize_role(role, user_type=None):
    if role == "recruiter" or user_type == "recruiter":
        return "employer"
    if role == "candidate" or user_type == "candidate":
        return "job_seeker"
    if role in ALLOWED_ROLES:
        return role
    return "job_seeker"


def make_token(user):
    now = datetime.now(timezone.utc)
    payload = {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(hours=1),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def _auth_error(message, status):
    return jsonify({"error": message}), status


def authenticate_token(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        token = parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None

        if not token:
            return _auth_error("Authentication token is required", 401)

        try:
            user = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        except jwt.PyJWTError:
            return _auth_error("Invalid or expired token", 403)

        g.user = user
        return view(*args, **kwargs)

    return wrapped


def authorize_roles(roles):
    role_set = set(roles)

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = getattr(g, "user", None)
            if not user:
                return _auth_error("Authentication token is required", 401)
            if user.get("role") not in role_set:
                return _auth_error("Insufficient permissions", 403)
            return view(*args, **kwargs)

        return wrapped

    return decorator

