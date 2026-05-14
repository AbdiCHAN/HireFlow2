import hashlib
import secrets

from flask import Blueprint, g, jsonify, request

from ..auth_utils import authenticate_token
from ..extensions import db
from ..models import ApiKey, utcnow

api_keys_bp = Blueprint("api_keys", __name__, url_prefix="/api/api-keys")


def hash_key(key):
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


@api_keys_bp.get("/")
@authenticate_token
def list_api_keys():
    keys = (
        ApiKey.query
        .filter_by(user_id=g.user.get("id"))
        .order_by(ApiKey.created_at.desc())
        .all()
    )
    return jsonify({"data": [key.to_public_dict() for key in keys]})


@api_keys_bp.post("/")
@authenticate_token
def create_api_key():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name") or "HireFlow API Key").strip() or "HireFlow API Key"
    raw_key = f"hf_{secrets.token_urlsafe(24)}"

    api_key = ApiKey(
        user_id=g.user.get("id"),
        name=name,
        key_hash=hash_key(raw_key),
        key_prefix=f"{raw_key[:8]}...",
    )
    db.session.add(api_key)
    db.session.commit()

    payload = api_key.to_public_dict()
    payload["key"] = raw_key
    return jsonify({
        "message": "API key created. Copy it now; it will not be shown again.",
        "data": payload,
    }), 201


@api_keys_bp.delete("/<key_id>")
@authenticate_token
def revoke_api_key(key_id):
    try:
        numeric_id = int(key_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid API key ID"}), 400

    api_key = (
        ApiKey.query
        .filter_by(id=numeric_id, user_id=g.user.get("id"), revoked_at=None)
        .first()
    )
    if not api_key:
        return jsonify({"error": "API key not found"}), 404

    api_key.revoked_at = utcnow()
    db.session.commit()
    return jsonify({"message": "API key revoked successfully"})
